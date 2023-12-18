import os


def rename_files_recursively(directory_path, old_name, new_name):
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if old_name == filename:
                # print("change ",filename)
                old_filepath = os.path.join(root, filename)
                new_filename = filename.replace(old_name, new_name)
                new_filepath = os.path.join(root, new_filename)
                os.rename(old_filepath, new_filepath)
                print(f'Renamed: {old_filepath} to {new_filepath}')

# 请替换下面的路径、旧文件名和新文件名
directory_path = '/raid/guan/hypergraph/simulation/test_data/'
old_name = 'anti-basic-edge.txt.bak'
new_name = 'bak-anti-basic'

rename_files_recursively(directory_path, old_name, new_name)
