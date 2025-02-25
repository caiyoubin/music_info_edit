import json
import os
from datetime import datetime
from typing import List


class JsonUtil:
    singers = []

    config_directory = r"..\config"
    json_filename = "music.json"

    # 合并路径和文件名
    @classmethod
    def get_json_path(cls) -> str:
        return os.path.join(cls.config_directory, cls.json_filename)

    # 获取歌手名字
    @classmethod
    def get_singers(cls) -> List[str]:
        if not cls.singers:
            cls.singers = cls.read_data(cls.get_json_path(), "singers")
        return cls.singers

    # 获取脏数据
    @classmethod
    def get_dirty_data(cls):
        return cls.read_data(cls.get_json_path(), "dirty_data")

    # 读取json文件中的指定数据
    @classmethod
    def read_data(cls, file_path: str, data_type: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
                return list(content.get(data_type, []))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            return []

    # 把歌手信息写入json文件中
    @classmethod
    def write_singer(
        cls,
        singers: List[str],
        file_name: str = "music.json",
    ):
        file_path = cls.get_json_path()
        try:
            # 读取文件内容
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)

            # 获取文件中已有的歌手列表
            existing_singers = content.get("singers", [])
            combined_singers = existing_singers + singers

            # 去重并排序
            unique_singers = sorted(set(combined_singers))

            # 更新文件内容
            content["singers"] = unique_singers
            content["add_size"] = len(unique_singers) - content.get("singer_size", 0)
            content["singer_size"] = len(unique_singers)
            content["last_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 写回文件
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=4, ensure_ascii=False)

            print(f"歌手信息已更新并写入文件 {file_path}")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"写入文件 {file_path} 时出错: {e}")
