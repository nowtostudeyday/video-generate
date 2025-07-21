import os
from queue import Queue

import requests

from zhipuai import ZhipuAI
from constants import constants


def create_agent():
    """
    创建智能体
    :return:
    """
    # 创建 client
    client = ZhipuAI(api_key=constants.API_KEY)
    return client


def generate_video(client: ZhipuAI, base64_image: str) -> str:
    """
    提交生成任务

    :param client: AI 客户端
    :param base64_image: base64 编码图片
    :return: 任务 ID
    """
    resp = client.videos.generations(
        model="CogVideoX-Flash",
        image_url=base64_image,
        prompt=constants.PROMPT,
        quality="quality",  # 输出模式，"quality"为质量优先，"speed"为速度优先
        with_audio=False,
        size="1080x1920",  # 视频分辨率，支持最高4K（如: "3840x2160"）
        fps=60,  # 帧率，可选为30或60
    )
    print(f"generate success, id=[{resp.id}]")
    return resp.id

def select_result(client: ZhipuAI, task_id: str, result_queue: Queue):
    while True:
        # 查询生成结果
        result = client.videos.retrieve_videos_result(id=task_id)
        if result.task_status == 'SUCCESS':
            # 获取对应 URL 路径
            video_result = result.video_result[0]
            print(f"result -> url=[{video_result.url}]")
            result_queue.put((video_result.url, task_id))
            return
        elif result.task_status != 'PROCESSING':
            print(f"result -> error=[{task_id}]")
            return


def download_video(video_url: str, save_folder: str, file_name: str) -> bool:
    """
    下载视频并保存到本地指定文件夹

    :param video_url: MP4 视频链接
    :param save_folder: 本地保存文件夹路径
    :param file_name: 保存的文件名
    :return: 保存成功返回 True，失败返回 False
    """
    # 确保保存文件夹存在
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    if not file_name.endswith(".mp4"):
        file_name += ".mp4"

    save_path = os.path.join(save_folder, file_name)

    try:
        # 发送请求获取视频内容
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        # 以二进制写入模式打开文件
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"视频已成功保存到: {save_path}")
        return True
    except requests.RequestException as e:
        print(f"下载视频时出现错误: {e}")
        return False
    except Exception as e:
        print(f"保存视频文件时出现错误: {e}")
        return False