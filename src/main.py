import os

from utils.json_util import JsonUtil


def change_name_site_reg(dir_path, reverse=False):
    files = os.listdir(dir_path)
    singers = JsonUtil.get_singers()

    for file in files:
        unchanged_name = list()
        if len(unchanged_name) > 3:
            break

        isdir = os.path.join(dir_path, file)

        # 不处理 unchanged 命名的目录
        if "unchanged" in dir_path:
            continue

        if os.path.isdir(isdir):
            # 把目录名字加到歌手列表, 因为有的目录以歌手名命名
            singers.append(file)
            change_name_site_reg(isdir)
            continue

        # 演唱者名字放在前面， 以 - 分割
        JsonUtil.change_name_site(
            file, dir_path, isdir, singers, unchanged_name, reverse
        )

    JsonUtil.write_singer(singers)


if __name__ == "__main__":

    # 可用 black your_project_directory 来整理代码风格
    # D:\code > black.\music_info_edit

    user_path = r"D:\Music"
    # user_path = r"D:\Music\Miscellaneous"
    # user_path = r"D:\Music\Instrumental Tracks"
    # user_path = r"D:\Music\Vocal Tracks"
    # user_path = r"D:\Documents\lyrics"
    # user_path = r"D:\Music\New folder - Copy"
    # user_path = r"D:\Music\New folder - Copy\unchanged - Copy"
    # user_path = r"D:\Music\test-can-del"

    # 存在 part1 与 part2 都在歌手列表中的情况, 概率较小, 出现时再手动处理
    # reverse 参数为 True , 则歌手名字在前, 歌曲名字在后, 默认为 False
    change_name_site_reg(
        user_path,
    )  # 演唱者名字放在前面， 以 - 分割

    # todo 分组, 个人单曲大于等于5, 单独放入个人目录

    # TODO 更改文件里的标签
    # 按照文件的后缀名来分别处理

    # TODO 自动更新 C:\temp\car_music 中的文件 , 更新之后顺带运行  sysnc_lyrics 脚本

    # 无法存入singer names
# 请输入歌手对应的数字：
# 1、Don't Know What To Do  2、BLACKPINK  3、(没有对应选项)
# 2
# 请输入歌手对应的数字：
# 1、热河 (2016 unplugged)  2、李志;朱格乐;张怡然  3、(没有对应选项)
# 2
