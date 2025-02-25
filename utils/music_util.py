import os

from utils.json_util import JsonUtil


class MusicUtil:

    singers = JsonUtil.get_singers()

    @classmethod
    def is_dirty_data(cls, string, dirty_data):

        # 数据为空 不算脏数据
        if not string:
            return False

        # 检查 string 是否在脏数据中
        if string in dirty_data:
            return True

        # 检查 string 是否是由不定长的 "?" 组成
        if (
            string.strip("?") == ""
        ):  # 如果 string 只包含 "?"，strip 会把所有 "?" 去掉，剩下空字符串
            return True

        return False

    @classmethod
    def get_singer_and_song(cls, file_name):
        """
        根据文件名确认歌手和歌曲的名字，并返回歌手和歌曲的名称。
        如果未能自动识别，会提示用户输入对应的数字。
        """
        if file_name.count(" - "):
            parts = file_name.split(" - ")
            if len(parts) != 2:
                return "", ""

            part1 = parts[0].strip()
            parts = parts[1].split(".")
            if len(parts) != 2:
                return "", ""
            part2 = parts[0].strip()

            singer = ""
            song = ""

            for name in cls.singers:
                if name == part1:
                    singer = part1
                    song = part2
                    break
                elif name == part2:
                    singer = part2
                    song = part1
                    break

            if len(singer) == 0:
                # 提示用户输入
                if "," in part1 and "," not in part2:
                    return part1, part2
                elif "," in part2 and "," not in part1:
                    return part2, part1
                else:
                    input_info = f"请输入歌手对应的数字：\n1、{part1}  2、{part2}  3、(没有对应选项)"
                    print(input_info)
                    receive = input()

                    if receive == "1":
                        singer = part1
                        song = part2
                        cls.singers.append(singer)
                    elif receive == "2":
                        singer = part2
                        song = part1
                        cls.singers.append(singer)
                    else:
                        return "", ""
            return (
                singer,
                song,
            )

        return "", ""

    @classmethod
    def rename_file(cls, file_name, file_path, isdir, singer, song, reverse):
        """
        根据歌手和歌曲名称重命名文件并移动到正确的文件夹。
        如果未符合规则，文件会被移动到 'unchanged' 文件夹。
        """
        if reverse:
            singer, song = song, singer
        suffix = "." + file_name.split(".")[-1]
        # 使用 song 和 singer 来重命名文件
        file_replace = f"{song} - {singer}{suffix}"  # 歌手名在后
        if file_name == file_replace:
            return
        new_dir = os.path.join(file_path, file_replace)

        try:
            os.rename(isdir, new_dir)
            print(
                isdir.replace(file_path, ""),
                "******",
                new_dir.replace(file_path, ""),
                end="\n\n",
            )
        except Exception as e:
            print(f"old name: {isdir}")
            print(f"new name: {new_dir}")
            print(f"Error: {e}")

    # 在调用这个方法之后要使用  JsonUtil.write_singer(JsonUtil.singers) 来保存新增的歌手
    @classmethod
    def change_name_site(cls, file_name, file_path, isdir, unchanged_name, reverse):
        singer, song = cls.get_singer_and_song(file_name)

        if singer and song:
            # 文件名已经识别并且修改
            cls.rename_file(file_name, file_path, isdir, singer, song, reverse)
        else:
            unchanged_name.append(file_name)
            print(f"文件未能更改: {file_name}")

            unchanged_path = os.path.join(file_path, "unchanged")
            if not os.path.exists(unchanged_path):
                os.mkdir(unchanged_path)
                print(f"Mkdir: {unchanged_path}")

            os.rename(
                os.path.join(file_path, file_name),
                os.path.join(unchanged_path, file_name),
            )
        cls.singers.append(singer)
