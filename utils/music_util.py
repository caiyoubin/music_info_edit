import os

from utils.json_util import JsonUtil


class MusicUtil:
    singers = JsonUtil.get_singers()

    @classmethod
    def is_dirty_data(cls, string, dirty_data) -> bool:

        # 数据为空 不算脏数据
        if not string:
            return False
        # 检查 string 是否在脏数据中
        if string in dirty_data:
            return True
        # 检查 string 是否是由不定长的 "?" 组成
        if string.strip("?") == "":  # 如果 string 只包含 "?"，strip 会把所有 "?" 去掉，剩下空字符串
            return True
        return False

    @classmethod
    def is_music_file(cls, file_name) -> bool:
        valid_extensions = {".flac", ".mp3", ".wav", ".m4a"}
        # 忽略大小写检查文件扩展名
        if not any(file_name.lower().endswith(ext) for ext in (".mp3", ".wav", ".flac")):
            return False
        return True

    @classmethod
    def get_singer_and_song(cls, file_name) -> (str, str):
        """
        根据文件名提取歌手和歌曲的名称。
        如果未能自动识别，会提示用户输入对应的数字。

        !!! 在函数调用此方法之后, 要在结束时调用JsonUtil 中的保存方法
        """
        if not cls.is_music_file(file_name):
            return "", ""

        segments = []
        if " - " in file_name:
            segments = file_name.split(" - ")
        elif "-" in file_name:
            segments = file_name.split("-")

        if len(segments) != 2:
            return "", ""

        first_part = segments[0].strip()
        segments = segments[1].rsplit(".", 1)
        if len(segments) != 2:
            return "", ""
        last_part = segments[0].strip()

        singer = ""
        song = ""

        for name in cls.singers:
            if name == first_part:
                singer = first_part
                song = last_part
                break
            elif name == last_part:
                singer = last_part
                song = first_part
                break

        if len(singer) == 0:
            # 提示用户输入
            if "," in first_part and "," not in last_part:
                return first_part, last_part
            elif "," in last_part and "," not in first_part:
                return last_part, first_part
            else:
                input_info = f"请输入歌手对应的数字：\n1、{first_part}  2、{last_part}  3、(没有对应选项)"
                print(input_info)
                user_input = input()

                if user_input == "1":
                    singer = first_part
                    song = last_part
                    cls.singers.append(singer)
                elif user_input == "2":
                    singer = last_part
                    song = first_part
                    cls.singers.append(singer)
                else:
                    return "", ""
        return singer, song

    @classmethod
    def rename_file(cls, file_name, file_path, isdir, singer, song, reverse) -> None:
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
            print(f"[重命名成功]{isdir.replace(file_path, "")} ==> {new_dir.replace(file_path, "")}", end="\n\n")
        except Exception as e:
            print(f"Error: {e}")

    # 在调用这个方法之后要使用  JsonUtil.write_singer(JsonUtil.singers) 来保存新增的歌手
    @classmethod
    def change_name_site(cls, file_name, file_path, isdir, unchanged_name, reverse) -> None:
        if not cls.is_music_file(file_name):
            return
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
