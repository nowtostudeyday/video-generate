import os
from queue import Queue
from constants import constants
from utils import *


def process_image(client, image_name: str, output_queue: Queue):
    """
    处理单个图片

    :param client: AI 客户端
    :param image_name: 图片名称
    :param output_queue: 输出队列
    :return:
    """
    print(f'start process image: {image_name}')
    image_file = os.path.join(constants.DEFAULT_INPUT_FOLDER, image_name)

    # 转换成 base64
    base64_str = image_util.image_to_base64(image_file)
    if not base64_str:
        output_queue.put((image_name, None, '转换图片为base64失败！'))
        return

    # 生成视频
    task_id = video_generate.generate_video(client, base64_str)

    if task_id:
        output_queue.put((image_name, task_id, None))
        print('+++', output_queue.qsize())

        # 删除对应图片
        image_util.delete_image(image_file)
    else:
        output_queue.put((image_name, None, '提交生成任务失败'))
        print(f"图片 {image_name} 处理失败")

def result_process(client, output_queue: Queue, result_queue: Queue) -> None:
    """
    获取生成结果

    :param client: AI 客户端
    :param output_queue: 输出队列
    :param result_queue: 结果队列
    :return: None
    """
    while True:
        image_name, task_id, error = output_queue.get()
        print('---', output_queue.qsize())
        try:
            if task_id:
                print(f"图片 {image_name} 处理中")
                video_generate.select_result(client, task_id, result_queue)
            else:
                print(f"图片 {image_name} 处理失败: {error}")
        finally:
            output_queue.task_done()