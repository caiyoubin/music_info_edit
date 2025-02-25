# 本脚本时针对car_music目录做了一个集中处理
from tools.sync_lyrics import sync_lyrics
from tools.clean_lrc_directory import (
    get_music_files_from_directory,
    clean_car_music_directory,
)
from tools.remove_by_tag_from_lrc import remove_by_tag_from_lrc


def main():
    # 第一步
    # 模块一：获取 D:\Music 中的所有文件名集合
    # 清理car_music中在歌库已删除的歌曲
    music_directory = r"D:\Music"
    valid_file_names = get_music_files_from_directory(music_directory)
    print(
        f"Collected {len(valid_file_names)} valid music file names from {music_directory}"
    )

    # 清理 C:\temp\car_music 中在歌库已删除的歌曲
    car_music_directory = r"C:\temp\car_music"
    valid_extensions = {".flac", ".mp3", ".wav", ".m4a"}

    clean_car_music_directory(car_music_directory, valid_file_names, valid_extensions)
    print(f"Finished cleaning {car_music_directory}")

    # 第二步
    # 清除歌词中的多余标签
    remove_by_tag_from_lrc()

    # 第三步
    # 同步 car_music 中的歌词
    sync_lyrics(r"C:\temp\car_music", r"D:\Documents\lyrics")


if __name__ == "__main__":
    main()
