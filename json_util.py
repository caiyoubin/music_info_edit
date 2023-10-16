import json
import os

# 读取json文件中的歌手信息
def read_singer(file_name):
    dir_path = os.getcwd() + "\\" + file_name
    # print(dir_path)
    with open(dir_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        return list(content["singer_name"])

# 把歌手信息写入json文件中
def write_singer(file_name, singer_name):
    dir_path = os.getcwd() + "\\" + file_name
    # print(dir_path)
    with open(dir_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    with open(dir_path, "w", encoding="utf-8") as f:
        singer_name.sort()
        content["singer_name"] = list(set(singer_name))
        content["singer_size"] = len(singer_name)
        json.dump(content, f, indent=4, ensure_ascii=False)
