import os


def replace_in_filename(directory):
    # 遍历目录及子目录
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 替换文件名中的字符
            new_filename = filename.replace('（', '(').replace('）', ')')

            # 如果文件名有变化，则重命名文件
            if new_filename != filename:
                old_file = os.path.join(root, filename)
                new_file = os.path.join(root, new_filename)
                os.rename(old_file, new_file)
                print(f'Renamed: {old_file} -> {new_file}')
                print()


if __name__ == '__main__':

    # 指定要扫描的目录
    directory = r'D:\Music'
    # 调用函数进行替换
    replace_in_filename(directory)

    directory = r'D:\Documents\lyrics'
    replace_in_filename(directory)
