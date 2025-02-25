"""
清理car_music中在歌库已删除的歌曲
"""

import os
import os.path
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


# 模块一：获取 D:\Music 中所有文件的文件名，存入 set 集合
def get_music_files_from_directory(path):
    file_names = set()
    for root, _, files in os.walk(path):
        for file in files:
            # 获取不包含后缀的文件名
            file_name_without_extension = os.path.splitext(file)[0]
            file_names.add(file_name_without_extension)
    return file_names


# 模块二：检查 C:\temp\car_music 目录中的文件，删除那些未在集合中的文件
def clean_car_music_directory(path, valid_file_names, valid_extensions):
    for root, _, files in os.walk(path):
        for file in files:
            # 检查文件后缀
            if os.path.splitext(file)[1].lower() in valid_extensions:
                file_name_without_extension = os.path.splitext(file)[0]
                # 如果文件名不在集合中，删除该文件
                if file_name_without_extension not in valid_file_names:
                    full_file_path = os.path.join(root, file)
                    # print(full_file_path)
                    try:
                        os.remove(full_file_path)
                        print(f"Deleted file: {full_file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting file {full_file_path}: {e}")


if __name__ == "__main__":
    # 模块一：获取 D:\Music 中的所有文件名集合
    music_directory = r"D:\Music"
    valid_file_names = get_music_files_from_directory(music_directory)
    print(
        f"Collected {len(valid_file_names)} valid music file names from {music_directory}"
    )

    # 模块二

    # 清理 C:\temp\car_music 中在歌库已删除的歌曲
    car_music_directory = r"C:\temp\car_music"
    valid_extensions = {".flac", ".mp3", ".wav", ".m4a"}

    # 清理歌词文件
    # car_music_directory = r"D:\Documents\lyrics"
    # valid_extensions = {'.lrc', '.txt'}

    clean_car_music_directory(car_music_directory, valid_file_names, valid_extensions)
    print(f"Finished cleaning {car_music_directory}")
