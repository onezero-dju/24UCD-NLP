import runpod
from runpod.serverless.utils.rp_validator import validate

# def handler(job):
#     job_input = job["input"]

#     return f"Hello {job_input['name']}!"



schema = {
    "text": {
        "type": str,
        "required": True,
    },
    "max_length": {
        "type": int,
        "required": False,
        "default": 100,
        "constraints": lambda x: x > 0,
    }
}

# def handler(event):
#     try:
#         validated_input = validate(event["input"], schema)
#         if 'errors' in validated_input:
#             return {"error": validated_input['errors']}
        
#         text = validated_input['validated_input']['text']
#         max_length = validated_input['validated_input']['max_length']
        
#         result = text[:max_length]
#         return {"output": result}
#     except Exception as e:
#         return {"error": str(e)}

# runpod.serverless.start({"handler": handler})

def process_data(text: str):
    return text[:2]

def handler(event):
    try:
        validated_input = validate(event["input"], schema)
        if 'errors' in validated_input:
            return {"error": validated_input['errors']}
        
        # Your processing logic here
        text = validated_input['validated_input']['text']
        result = process_data(text)
        
        return {"custom_output": result}  # Custom schema
    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})