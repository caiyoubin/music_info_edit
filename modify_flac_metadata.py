import os
import traceback
from pathlib import Path

from mutagen.flac import FLAC
from mutagen.flac import FLACNoHeaderError

from utils.json_util import JsonUtil
from utils.music_util import MusicUtil


# 1. 文件处理模块
def get_flac_files(directory):
    """
    遍历目录及子目录，返回所有 .flac 文件的路径列表。
    """
    flac_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".flac"):
                flac_files.append(os.path.join(root, file))
    return flac_files


# 2. FLAC 文件元数据处理模块
def modify_metadata(file_path):
    """
    修改 FLAC 文件的元数据（标题、艺术家、专辑）。
    """
    singer, song = MusicUtil.get_singer_and_song(Path(file_path).name)
    # print(file_path)
    if not singer or not song:
        # 如果没有歌手或歌曲信息，返回
        return
    dirty_data = JsonUtil.get_dirty_data()
    try:
        audio = FLAC(file_path)
    except FLACNoHeaderError as e:
        print(f"文件 {file_path} 不是有效的 FLAC 文件，跳过此文件。", {e})
        return  # 跳过此文件，继续处理下一个文件

    try:
        # 捕获 FLACNoHeaderError 错误并处理

        # 使用 get 方法安全地获取元数据
        title = audio.get("title", [None])[0]
        artist = audio.get("artist", [None])[0]
        album = audio.get("album", [None])[0]

        # 函数：检查并更新字段（如果脏数据）
        def update_field(field_name, field_value, new_value):
            if MusicUtil.is_dirty_data(field_value, dirty_data):
                audio[field_name] = new_value
                return True
            return False

        flag = False

        # 更新 title 和 artist
        flag |= update_field("title", title, song)
        flag |= update_field("artist", artist, song)

        # 如果 album 不是空的，才进行修改
        if album and MusicUtil.is_dirty_data(album, dirty_data):
            audio["album"] = ""
            flag = True

        # 如果有任何修改，保存文件
        if flag:
            audio.save()
            print(f"成功修改元数据: {file_path}")
    except Exception as e:
        traceback.print_exc()  # 打印完整的异常堆栈
        print(f"无法修改文件 {file_path}: {e}")


# 3. 主程序
def main():
    # 设置需要处理的目录
    directory = r"D:\Music\New folder - Copy"
    directory = r"D:\Music\New folder - Copy\unchanged - Copy"
    directory = r"D:\Music"
    # directory = r"C:\temp\car_music"

    # 获取目录下所有 FLAC 文件
    flac_files = get_flac_files(directory)

    # 修改每个 FLAC 文件的元数据
    for file_path in flac_files:
        modify_metadata(file_path)
    JsonUtil.write_singer(JsonUtil.singers)


# 执行主程序
if __name__ == "__main__":
    main()
