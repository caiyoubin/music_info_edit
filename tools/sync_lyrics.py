"""
同步 car_music 中的歌词：

1. 获取音乐文件和歌词文件：从指定的文件夹中获取音乐和歌词文件，并根据后缀筛选。
2. 删除已存在的歌词文件：在运行脚本前，删除音乐目录下所有已有的 .lrc 文件。
3. 根据忽略文件跳过文件：从 sync_lyrics_ignore_music.txt 文件中读取需要跳过的文件（去掉前缀 - ），
   如果音乐文件名在其中，就不进行处理。
4. 复制匹配的歌词文件：将匹配的歌词文件复制到对应的音乐文件目录中。
5. 输出未匹配的文件：如果某些音乐文件没有找到匹配的歌词文件，输出这些文件名。
"""

import os
import shutil
from pathlib import Path


def get_music_files(music_dir):
    """
    获取指定音乐文件夹下的所有音乐文件（mp3, wav, flac），忽略大小写。

    参数:
    music_dir (str): 音乐文件夹路径。

    返回:
    list: 包含所有音乐文件的元组，每个元组包含文件名（不带后缀）、文件所在目录和完整的文件名。
    """
    music_files = []
    print(f"开始扫描音乐文件夹: {music_dir}...")
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith(("mp3", "wav", "flac")):
                # 获取文件名，不包括后缀
                music_files.append((os.path.splitext(file)[0].lower(), root, file))
    print(f"共发现 {len(music_files)} 个音乐文件.")
    return music_files


def get_lyrics_files(lyrics_dir):
    """
    获取指定歌词文件夹下的所有 .lrc 文件，忽略大小写。

    参数:
    lyrics_dir (str): 歌词文件夹路径。

    返回:
    list: 包含所有歌词文件的元组，每个元组包含文件名（不带后缀）和文件的完整路径。
    """
    lyrics_files = []
    print(f"\n开始扫描歌词文件夹: {lyrics_dir}...")
    for root, dirs, files in os.walk(lyrics_dir):
        for file in files:
            if file.lower().endswith(".lrc"):
                lyrics_files.append(
                    (os.path.splitext(file)[0].lower(), os.path.join(root, file))
                )
    return lyrics_files


def delete_existing_lyrics(music_dir):
    """
    删除音乐目录中所有的 .lrc 文件。

    参数:
    music_dir (str): 音乐文件夹路径。
    """
    print(f"\n删除音乐文件夹 {music_dir} 中的所有歌词文件...")
    deleted_files = 0
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith(".lrc"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                deleted_files += 1
    print(f"共删除 {deleted_files} 个歌词文件.")


def read_sync_lyrics_ignore_file(ignore_file_path):
    """
    读取文件，返回忽略的歌词文件名列表。

    参数:
    ignore_file_path (str): 忽略文件路径。

    返回:
    set: 忽略的文件名集合。
    """
    ignored_files = set()
    if os.path.exists(ignore_file_path):
        with open(ignore_file_path, "r", encoding="utf-8") as file:
            for line in file:
                ignored_files.add(line.strip())  # 去掉空格
    else:
        print("读取不到 sync_lyrics_ignore_music.txt")
    return ignored_files


def copy_lyrics_to_music(music_files, lyrics_files, ignored_files):
    """
    将匹配的歌词文件复制到对应的音乐文件目录。

    参数:
    music_files (list): 包含所有音乐文件的元组。
    lyrics_files (list): 包含所有歌词文件的元组。
    ignored_files (set): 需要忽略的文件名集合。

    返回:
    tuple: 包含两个元素：
        - 复制的歌词文件数量
        - 未匹配的音乐文件列表
    """

    lyrics_copied = 0
    unmatched_music_files = []
    for music_name, music_dir, music_file in music_files:
        matched = False
        for lyric_name, lyric_path in lyrics_files:
            if lyric_name == music_name:
                # 复制.lrc文件到音乐文件所在的目录
                shutil.copy(
                    lyric_path, os.path.join(music_dir, os.path.basename(lyric_path))
                )
                lyrics_copied += 1
                matched = True
                break  # 一旦找到匹配就可以跳出内部循环
        if not matched:
            if music_file in ignored_files:
                continue
            unmatched_music_files.append(music_file)
            # 误删除电脑中的全部lrc时, 快速获取car_music中未有的歌词
            # C:\temp\car_music\1  手动保证路径里的目录存在
            # shutil.copy(os.path.join(music_dir, music_file), os.path.join(r"C:\temp\car_music\1", music_file))
    return lyrics_copied, unmatched_music_files


def sync_lyrics(music_dir, lyrics_dir):
    """
    主函数，执行脚本的主要流程：读取文件，删除已有的歌词文件，复制匹配的歌词文件，并输出未匹配的文件。
    """

    ignore_file_path = Path("D:/code/music_info_edit/config/sync_lyrics_ignore_music.txt")
    if not ignore_file_path.exists():
        print("文件不存在，请检查路径")

    # 读取忽略的歌词文件名
    ignored_files = read_sync_lyrics_ignore_file(ignore_file_path)
    # 删除音乐目录中现有的歌词文件
    delete_existing_lyrics(music_dir)

    # 获取音乐文件和歌词文件
    music_files = get_music_files(music_dir)
    lyrics_files = get_lyrics_files(lyrics_dir)

    # 将歌词文件复制到对应的音乐文件目录
    lyrics_copied, unmatched_music_files = copy_lyrics_to_music(
        music_files, lyrics_files, ignored_files
    )

    print(f"\n任务完成. 共复制了 {lyrics_copied} 个歌词文件.")

    if unmatched_music_files:
        print("\n以下歌曲未找到匹配的歌词文件:")
        for music_file in sorted(unmatched_music_files):
            print(f"{music_file}", "\n")


if __name__ == "__main__":

    # 更新car_music中的歌词
    music_dir = r"C:\temp\car_music"
    lyrics_dir = r"D:\Documents\lyrics"
    sync_lyrics(music_dir, lyrics_dir)
