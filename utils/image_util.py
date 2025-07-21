import os
import base64
from typing import Union


def image_to_base64(image_path) -> Union[str, None]:
    """
    读取本地图片并转换为Base64编码

    :param image_path:  本地路径
    :return: Base64 编码
    """
    try:
        with open(image_path, 'rb') as image_file:
            encoded_str = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_str
    except Exception as e:
        print(f"Error reading image: {e}")
        return None


def get_images(folder: str) -> list[str]:
    """
    获取 input 图片集合

    :param folder: 文件夹路径
    :return: 图片集合
    """
    return [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

def delete_image(image_file: str) -> None:
    """
    删除对应图片

    :param image_file: 图片路径
    :return: None
    """
    os.remove(image_file)