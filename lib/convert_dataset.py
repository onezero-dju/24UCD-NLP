import csv
from dspy.datasets import DataLoader
from logging import basicConfig as logger_config, getLogger, DEBUG
from pathlib import Path


logger_config(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)


def get_dataset_base_path(dataset_name: str) -> None | Path:
    dataset_base_path = Path(__file__, f"../../data/_original/{dataset_name}").resolve()
    if not dataset_base_path.exists():
        logger.error(f"Can't find the dataset. Check the path: '{str(dataset_base_path)}'")
        return None
    else:
        logger.info(f"Dataset found on path: '{str(dataset_base_path)}'")
        return dataset_base_path


def convert_json_data(dataset_name: str, path_to_data: str):
    dataset_base_path = get_dataset_base_path(dataset_name)
    
    # Initialize DataLoader (DSPy)
    dl = DataLoader()

    json_data_dir = dataset_base_path / path_to_data
    
    if json_data_dir.exists() == False:
        logger.error("Can't find the json file")
    
    # Prepare to extract features from nested attributes
    all_features = []

    for file_path in json_data_dir.glob('*.json'):  # iterate through json files
    
        # Load JSON dataset
        json_dataset = dl.from_json(file_path=str(file_path))
    
        for data in json_dataset:
            # Access nested fields
            doc_id = data["Meta(Acqusition)"]["doc_id"]
            context = data["Meta(Refine)"]["passage"]  # Example of accessing a nested attribute
            summary = data["Annotation"]["summary1"]   # Another example of nested access
            # Append the extracted features to a list as a tuple
            all_features.append((doc_id, context, summary))

    # Export features to a CSV file
    with open("dataset.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        # Write header
        writer.writerow(["Document ID", "Context", "Summary"])
        # Write data rows
        writer.writerows(all_features)


if __name__ == "__main__":
    dataset_name = "ds01--aihub-582--report_gen"
    convert_json_data(dataset_name, path_to_data="train/04.paper/2~3sent/")
# end main

'''
현재는 하나의 디렉토리에 여러 JSON 파일로 데이터 단위가 나뉜 데이터셋에 대해, 각 파일들에 걸쳐서 데이터를 추출해 CSV로 합친다.
하지만 데이터셋의 특성에 따라 하나의 JSON에 여러 속성으로 데이터 튜플을 구분할 수도 있다.
# TODO: 후자의 경우에도 대응(형식 변환)할 수 있는 코드를 작성한다. + 다양한 데이터셋 구조에 대응 가능한 추상화 부여

현재는 `all_features` 리스트에 데이터를 넣어놓은 뒤에 이를 통해 CSV 파일을 생성하는, 다소 메모리를 많이 잡아먹는 구조이다.
# TODO: generator function을 이용해 메모리 사용량을 줄일 수 있는 방법을 모색한다.
'''
