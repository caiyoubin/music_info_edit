import os

from utils.json_util import JsonUtil
from utils.music_util import MusicUtil


def change_name_site_reg(file_path, reverse=False):
    files = os.listdir(file_path)
    singers = JsonUtil.get_singers()

    for file in files:
        unchanged_name = list()
        if len(unchanged_name) > 3:
            break

        isdir = os.path.join(file_path, file)

        # 不处理 unchanged 命名的目录
        if "unchanged" in file_path:
            continue

        if os.path.isdir(isdir):
            change_name_site_reg(isdir)
            continue

        # 演唱者名字放在前面， 以 - 分割
        MusicUtil.change_name_site(file, file_path, isdir, unchanged_name, reverse)


if __name__ == "__main__":

    # 可用 black your_project_directory 来整理代码风格
    # D:\code > black.\music_info_edit

    user_path = r"D:\Music"
    # user_path = r"D:\Music\Miscellaneous"
    # user_path = r"D:\Music\Instrumental Tracks"
    # user_path = r"D:\Music\Vocal Tracks"
    # user_path = r"D:\Documents\lyrics"

    # 存在 part1 与 part2 都在歌手列表中的情况, 概率较小, 出现时再手动处理
    # reverse 参数为 True , 则歌手名字在前, 歌曲名字在后, 默认为 False
    change_name_site_reg(
        user_path,
    )  # 演唱者名字放在前面， 以 - 分割

    JsonUtil.write_singer(JsonUtil.get_singers())
    # todo 分组, 个人单曲大于等于5, 单独放入个人目录

    # TODO 更改文件里的标签
    # 按照文件的后缀名来分别处理
