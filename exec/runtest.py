import os

dataset_list = []
method_list = ["basic","anti_basic","entropy","MinMax","HYPE","KaHypar"]
cur_path = os.getcwd()+"/../data/"

for method in method_list:
    for dataset in dataset_list:
