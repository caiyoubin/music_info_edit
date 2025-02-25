import json
import os
from datetime import datetime


class JsonUtil:
    singers = []

    config_directory = "../config"
    json_filename = "music.json"
    # 合并路径和文件名
    json_path = os.path.join(config_directory, json_filename)



    # 获取歌手名字
    @classmethod
    def get_singers(cls):
        if not cls.singers:
            cls.singers = cls.read_data(cls.json_path, "singers")
            return cls.singers
        return cls.singers

    # 获取脏数据
    @classmethod
    def get_dirty_data(cls):
        return cls.read_data(cls.json_path, "dirty_data")

    @classmethod
    def read_data(cls, file_name, data_type):
        dir_path = os.getcwd() + "\\" + file_name
        with open(dir_path, "r", encoding="utf-8") as f:
            content = json.load(f)
            return list(content[data_type])

    # 把歌手信息写入json文件中
    @classmethod
    def write_singer(
        cls,
        singers,
        file_name="music.json",
    ):
        dir_path = os.getcwd() + "\\" + file_name
        # print(user_path)
        with open(dir_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        # 获取文件中已有的歌手列表
        existing_singers = content.get("singers", [])
        # 将传入的歌手列表与已有的歌手列表合并
        combined_singers = existing_singers + singers
        # 去重并转换为集合，然后再转换回列表
        unique_singers = list(set(combined_singers))
        # 对歌手列表进行排序
        unique_singers.sort()

        with open(dir_path, "w", encoding="utf-8") as f:
            # 将合并、去重、排序后的歌手列表存入 content
            content["singers"] = unique_singers
            # 计算新增的歌手数量
            content["add_size"] = len(unique_singers) - content.get("singer_size", 0)
            # 更新歌手总数
            content["singer_size"] = len(unique_singers)
            # 更新最后修改时间
            content["last_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 将更新后的内容写入文件
            json.dump(content, f, indent=4, ensure_ascii=False)
