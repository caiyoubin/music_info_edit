import os

from json_util import read_singer, write_singer


# 演唱者名字放在前面， 以 - 分割
def change_name_site_reg(path):
    files = os.listdir(path)
    singer_name = list()
    singer_name.extend(read_singer("music.json"))

    unchanged_name = list()
    for file in files:
        if len(unchanged_name) > 3:
            break

        dir = os.path.join(path, file)
        if os.path.isdir(dir):
            change_name_site_reg(dir)
            continue

        if file.count(" - "):
            split = file.split(" - ")
            if len(split) != 2:
                unchanged_name.append(file)
                continue
            par1 = split[0].strip()

            split = split[1].split(".")
            if len(split) != 2:
                unchanged_name.append(file)
                continue
            par2 = split[0].strip()

            singer = ""
            song = ""
            flag = False

            for temp_name in singer_name:
                if temp_name == par1:
                    singer = par1
                    flag = True
                    break
                elif temp_name == par2:
                    singer = par2
                    song = par1
                    break

            if len(singer) == 0:

                if ',' in par1 and ',' not in par2:
                    receive = "1"
                elif ',' in par2 and ',' not in par1:
                    receive = "2"
                else:
                    input_info = "请输入歌手对应的数字：\n1、{0}  2、{1}  3、(没有对应选项)".format(par1, par2)
                    print(input_info)
                    receive = input()

                if receive == "1":
                    singer = par1
                    flag = True
                    singer_name.append(singer)
                elif receive == "2":
                    singer = par2
                    song = par1
                    singer_name.append(singer)
                else:
                    unchanged_name.append(file)
                    continue

            if flag:
                continue

            suffix = "." + split[1]
            file_replace = singer + " - " + song + suffix
            new_dir = os.path.join(path, file_replace)
            try:
                os.rename(dir, new_dir)
            except:
                print("************************  warning  *******************")
                print("old name: " + dir)
                print("new name: " + new_dir)
            print(dir.replace(path, ""), "******", new_dir.replace(path, ""), end='\n\n')

    # 未能更改的歌曲单独移动到一个目录
    print("未符合改名规则的歌曲: " + str(unchanged_name))
    if len(unchanged_name) > 0:
        unchanged_path = os.path.join(path, "unchanged")
        print("unchanged_path 1: " + unchanged_path)
        if not os.path.exists(unchanged_path):
            os.mkdir(unchanged_path)
            print("unchanged_path 2: " + unchanged_path)

        for temp_name in unchanged_name:
            os.rename(os.path.join(path, temp_name), os.path.join(unchanged_path, temp_name))

    write_singer("music.json", singer_name)


if __name__ == '__main__':

    file_path = "D:\\Music\\New folder - Copy\\"
    change_name_site_reg(file_path)  # 演唱者名字放在前面， 以 -   分割
