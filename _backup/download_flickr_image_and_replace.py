import os
import re
import requests

# 设置要遍历的目录
dir_path = '../_posts/'

# 定义正则表达式匹配图片行和flickr图片url
img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
flickr_pattern = re.compile(r'staticflickr\.com')


def get_count(count, all_image_url):
    if len(all_image_url) <= 9:
        return count
    elif len(all_image_url) <= 99:
        return f"0{count}" if count < 10 else count
    else:
        raise Exception("图片数量超过99张")


def handle_file(file: str, root: str):
    # 定义计数器，用于生成文件名
    count = 1

    file_path = os.path.join(root, file)
    # 读取文件内容
    with open(file_path, 'r') as f:
        content = f.read()

    # 查找图片行并下载flickr图片
    all_image_url = img_pattern.findall(content)
    for img_url in all_image_url:
        if flickr_pattern.search(img_url):
            response = requests.get(img_url)

            # 生成新的文件名
            new_name = f'{os.path.splitext(file)[0]}_{get_count(count, all_image_url)}{os.path.splitext(img_url)[1]}'

            # 保存图片并替换原来的url
            with open(os.path.join(root, new_name), 'wb') as f:
                f.write(response.content)
            content = content.replace(img_url, new_name)

            # 更新计数器
            count += 1
            print(f"处理文件{file_path}中，已下载{count - 1}张图片")
    # 将修改后的内容写入文件
    with open(file_path, 'w') as f:
        f.write(content)

    if count > 1:
        print(f"处理文件{file_path}成功，共替换{count - 1}张图片")

    return count


def handle_all():
    # 遍历目录下所有md文件
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.md'):
                count = handle_file(file, root)
                # if count > 1:
                #     exit()

'''
[x] 递归遍历目录， 找到所有 md 文件，找到 ![]() 格式的图片
[x] 下载, image 目录
[x] 重命名，前缀(文件名，url, 时间)，后缀，自增?
[x] 替换 url, 本地预览 + github 能用
[x] a/b test 先搞一个文件试试
[x] 本地格式替换 /images/qiniu-trail-151205hangzhou-25 替换为 ../images/mac_finder_sort_photos_by_taken_time_1
'''
if __name__ == '__main__':
    handle_all()
    # handle_file('2014-04-10-my_favourite_tshirt.md', '../_posts/')
