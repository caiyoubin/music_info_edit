import os
import re


def remove_by_tag(lyrics_folder, conditions):
    """
    删除所有包含 [by: 标签的行。

    :param conditions:
    :param lyrics_folder: 歌词文件夹的路径
    """
    if not os.path.exists(lyrics_folder):
        raise FileNotFoundError(f"目录 {lyrics_folder} 不存在。")

    # 遍历文件夹中的所有 .lrc 文件
    for filename in os.listdir(lyrics_folder):
        if filename.endswith(".lrc"):
            file_path = os.path.join(lyrics_folder, filename)
            try:
                # 读取文件内容
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                modified_lines = []
                deleted_lines = []

                # 遍历每行并处理
                for line in lines:
                    if any(cond in line for cond in conditions):
                        deleted_lines.append(line.strip())  # 保存被删除的行
                        continue

                    modified_lines.append(line)

                # 打印被删除的行
                if deleted_lines:
                    print(f"delete by:" + filename)
                    for line in deleted_lines:
                        print(line)

                # 如果文件有修改，保存文件
                if deleted_lines:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.writelines(modified_lines)
                    # print(f"保存文件：{filename}" + "\n")

            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")


def clean_timestamps(lyrics_folder):
    """
    清理歌词文件中的时间戳，只保留第一个时间戳，删除其余时间戳。
    如果行中只有一个时间戳，或者多个时间戳之间没有内容（包括空格），跳过该行。

    :param lyrics_folder: 歌词文件夹的路径
    """
    if not os.path.exists(lyrics_folder):
        raise FileNotFoundError(f"目录 {lyrics_folder} 不存在。")

    # 正则表达式匹配时间戳：[mm:ss.xx]
    timestamp_pattern = r"[\[\<]\d{2}:\d{2}\.\d{2}[\]\>]"
    # 遍历文件夹中的所有 .lrc 文件
    for filename in os.listdir(lyrics_folder):
        if filename.endswith(".lrc"):
            file_path = os.path.join(lyrics_folder, filename)
            try:
                # 读取文件内容
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                modified_lines = []

                flag = False
                # 遍历每行并处理
                for line in lines:
                    line = line.strip()
                    # 找到行中的所有时间戳
                    timestamps = re.findall(timestamp_pattern, line)

                    # 如果没有时间戳或只有一个时间戳，跳过此行
                    if len(timestamps) <= 1:
                        modified_lines.append(line + "\n")
                        continue

                    # 如果多个时间戳之间没有内容（即时间戳之间没有文字或只有空格）
                    stripped_line = re.sub(timestamp_pattern, "", line).strip()
                    if not stripped_line:  # 如果删除时间戳后没有任何内容（只剩空格）
                        modified_lines.append(line + "\n")
                        continue

                    # 获取时间戳之间的内容，先按时间戳分割
                    parts = re.split(timestamp_pattern, line)

                    # 使用列表推导式筛选非空项
                    non_empty_items = [item for item in parts if item]

                    if len(non_empty_items) > 1:
                        # 拼接非空项为一个字符串（用空格分隔）
                        first_timestamp = timestamps[0]  # 保留第一个时间戳
                        line = "".join(non_empty_items)
                        line = first_timestamp + line
                        modified_lines.append(line + "\n")
                        flag = True
                    else:
                        modified_lines.append(line + "\n")

                # 保存修改后的内容
                if flag:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.writelines(modified_lines)
                    print(f"已修改：{filename}")

            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")


def remove_by_tag_from_lrc():
    lyrics_folder = r"D:\Documents\lyrics"  # 这里填写你的文件夹路径

    # 先删除 指定标签的行
    conditions = ["[by:", "[id:", "[hash:", "[qq:", "[total:"]
    remove_by_tag(lyrics_folder, conditions)

    # 然后处理时间戳
    clean_timestamps(lyrics_folder)


if __name__ == "__main__":
    remove_by_tag_from_lrc()
    print("--done--")
