import os
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from queue import Queue

import constants.constants as const
from utils import *
from workers import processor


def main():
    start_time = datetime.now()

    # 创建 AI
    client = video_generate.create_agent()

    # 获取图片信息
    image_files: list[str] = image_util.get_images(const.DEFAULT_INPUT_FOLDER)
    print(f"fond {len(image_files)} size images, start generate video, start time: {start_time.strftime('%H:%M:%S')}")

    # 创建输出队列
    output_queue = Queue()
    result_queue = Queue()

    # 异步启动线程
    with ThreadPoolExecutor(max_workers=const.THREAD_NUM) as executor:
        for image_path in image_files:
            executor.submit(processor.process_image, client, image_path, output_queue)

    # 创建监控线程
    result_thread = threading.Thread(target=processor.result_process,
                                     args=(client, output_queue, result_queue))
    result_thread.daemon = True  # 设置为守护线程
    result_thread.start()

    # 等待所有任务完成
    output_queue.join()

    result_thread.join(timeout=60)

    # 保存视频到本地
    print(f"result_queue size: [{result_queue.qsize()}]")
    while not result_queue.empty():
        item = result_queue.get()
        video_generate.download_video(item[0], const.DEFAULT_OUTPUT_FOLDER, item[1])

    end_time = datetime.now()
    print(f"All Images Have Been Processed, timeConsuming: {end_time - start_time}")


if __name__ == '__main__':
    main()
