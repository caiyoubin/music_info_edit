import os
import shutil
from pathlib import Path
from typing import Dict, List

from utils.json_util import JsonUtil
from utils.music_util import MusicUtil


def find_directories(root_dir: str, ignore_list: List[str] = None) -> Dict[str, str]:
    """
    遍历指定目录下的所有子目录，并返回一个字典。
    key 为目录名，value 为目录路径。如果目录名重复，则保存层级最浅的路径。
    如果目录名在 ignore_list 中，则忽略该目录及其所有子目录。
    """
    if ignore_list is None:
        ignore_list = []  # 如果未提供 ignore_list，则初始化为空列表

    # 将 ignore_list 转换为小写并去重
    ignore_set = {item.lower() for item in ignore_list}

    dir_dict = {}

    # 将根目录添加到字典中
    root_name = os.path.basename(root_dir)
    if root_name.lower() not in ignore_set:
        dir_dict[root_name] = (0, root_dir)  # 根目录深度为 0

    for root, dirs, _ in os.walk(root_dir):
        current_depth = root.count(os.sep)  # 计算当前目录的深度

        # 动态修改 dirs，移除需要忽略的目录（大小写不敏感）
        dirs[:] = [d for d in dirs if d.lower() not in ignore_set]

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if dir_name not in dir_dict:
                dir_dict[dir_name] = (current_depth, dir_path)  # 保存深度和路径
            else:
                # 如果当前目录深度更小，则更新路径
                if current_depth < dir_dict[dir_name][0]:
                    dir_dict[dir_name] = (current_depth, dir_path)

    # 只保留路径，去掉深度信息
    return {k: v[1] for k, v in dir_dict.items()}


def filter_singer_directories(dir_dict: Dict[str, str], singers: List[str]) -> Dict[str, str]:
    """
    根据 singers 列表过滤目录字典，将匹配的目录移动到 singer_dic 中，并从原字典中移除。
    """
    singer_dic = {}
    for singer in singers:
        if singer in dir_dict:
            singer_dic[singer] = dir_dict.pop(singer)
    return singer_dic


def move_files_to_singer_dirs(dir_dict: Dict[str, str], singer_dic: Dict[str, str]) -> Dict[str, List[str]]:
    """
    遍历原字典中的路径，将文件名包含 singer_dic 中 key 的文件移动到对应的目录下。
    如果目标目录中已存在同名文件，则打印两个路径并跳过该文件。
    只遍历指定目录下的文件，不进入子目录。
    """
    file_path_dict = {}
    keys = singer_dic.keys()
    for dir_path in dir_dict.values():

        # 遍历当前目录下的文件（不进入子目录）
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            # 只处理文件，跳过目录
            if not os.path.isfile(file_path):
                continue

            # 解析文件名，获取歌手名字
            file_singer, _ = MusicUtil.get_singer_and_song(file_name)

            # 检查文件是否属于某个歌手
            if file_singer in keys:
                src_file_path = file_path
                dest_dir = singer_dic.get(file_singer)  # 目标目录
                dest_file_path = os.path.join(dest_dir, file_name)

                # 如果文件已经在目标目录中，跳过
                if os.path.dirname(src_file_path) == dest_dir:
                    print(f"文件已在目标目录，跳过: {src_file_path}")
                    continue

                # 如果目标文件已存在，打印路径并跳过
                if os.path.exists(dest_file_path):
                    print(f"文件已存在，跳过移动：")
                    print(f"源文件路径: {src_file_path}")
                    print(f"目标文件路径: {dest_file_path}")
                    continue

                # 移动文件
                shutil.move(src_file_path, dest_file_path)
                print(f'Moved {src_file_path} to {dest_file_path}')
                print()
            else:
                if file_singer not in file_path_dict:
                    file_path_dict[file_singer] = []
                file_path_dict[file_singer].append(file_path)

    return file_path_dict


def create_dir_and_move(root_dir: str, file_path_dict: Dict[str, List[str]], count: int = 5):
    # 将 root_dir 转换为 Path 对象
    root_dir = Path(root_dir)

    for key, value in file_path_dict.items():
        if len(value) == count:
            new_dir_path = root_dir / key
            # 创建目录（如果目录不存在）
            if not new_dir_path.exists():
                new_dir_path.mkdir(parents=True, exist_ok=True)
            for file_path in value:
                file_name = Path(file_path).name
                dest_file_path = new_dir_path / file_name
                shutil.move(file_path, dest_file_path)
                print(f'Moved {file_path} to {dest_file_path}')


def main():
    # 定义根目录
    root_dir = r'D:\Music'

    ignore_list = [""]
    # 步骤 1: 遍历目录并填充 dir_dict
    dir_dict = find_directories(root_dir, ignore_list)

    # 定义 singers 列表
    singers = JsonUtil.get_singers()

    # 步骤 2: 过滤出 singer_dic
    singer_dic = filter_singer_directories(dir_dict, singers)

    # 步骤 3: 移动文件到对应的歌手目录
    file_path_dict = move_files_to_singer_dirs(dir_dict, singer_dic)

    # 步骤 4: 单个演唱者的文件数大于等于指定数(默认 5), 创建文件夹, 并把文件移入
    create_dir_and_move(root_dir, file_path_dict, )

    JsonUtil.write_singer(singers)
    print("文件整理完成！")


if __name__ == "__main__":
    main()
