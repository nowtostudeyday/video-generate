import os

# 默认 input 输入文件夹
DEFAULT_INPUT_FOLDER = "D:\\python编程\\video-generate-from-pic\\inputPic"

# 默认 output 输出文件夹
DEFAULT_OUTPUT_FOLDER = "D:\\python编程\\video-generate-from-pic\\outputVideo"

# 线程个数
THREAD_NUM = 3

# API_KEY
API_KEY = os.getenv('API_KEY')

# 提示词  默认：人物自然走动
PROMPT = '让人物飞起来'