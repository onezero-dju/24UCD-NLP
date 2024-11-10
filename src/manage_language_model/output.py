
def to_print(input):
    pass

def to_txt(input):
    pass

def to_csv(input):
    pass

# mode_dict = {
#     0: to_print,
#     1: to_txt,
#     2: to_csv
# }

PRINT = to_print
TXT   = to_txt
CSV   = to_csv

def batch_output(dataset, scope: range, model, output_func: function):
    output_func()


# batch_output(data, range(10), model, TXT)