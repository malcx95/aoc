
def read_input(fname, data_type):
    nums = []
    with open("input.txt") as f:
        nums = [data_type(x) for x in f.readlines()]
    return nums 
