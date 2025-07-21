# 🎥 Image-to-Video Generator

基于智谱AI CogVideoX-Flash模型的图片转视频工具，支持批量处理与多线程加速，可将静态图片自动转换为动态视频。


## 项目概述 📝

本项目通过集成AI生成模型与自动化处理逻辑，实现了从图片输入到视频输出的全流程自动化。核心流程包括：本地图片读取→格式转换→AI视频生成→任务状态监控→视频下载存储。借助多线程并行处理能力，可高效完成批量图片的视频化转换，适用于插画动态展示、设计稿动效预览、人物图像动态化等场景。


## 核心功能 ✨

- **🚀 批量处理能力**：自动识别输入文件夹中所有支持的图片格式（PNG、JPG、JPEG、GIF），无需手动逐一操作；
- **🎨 AI动态生成**：基于智谱AI CogVideoX-Flash模型，通过提示词精准控制视频动态效果（如“让人物飞起来”“镜头缓慢推进”）；
- **⚡️ 多线程加速**：通过线程池并行处理任务，大幅提升批量处理效率，支持自定义线程数适配硬件性能；
- **🔄 全流程自动化**：包含图片转码、任务提交、状态查询、视频下载、源图清理等完整环节，零手动干预；
- **🛠️ 参数可配置**：支持自定义输入输出路径、线程数、视频质量（质量/速度优先）、分辨率（最高4K）、帧率（30/60fps）等核心参数。


## 技术栈 🛠️

- **编程语言**：Python 3.8+
- **AI模型**：智谱AI CogVideoX-Flash（图片转视频生成模型）
- **核心依赖**：`zhipuai`（智谱AI SDK）、`requests`（网络请求）、`base64`（图片编码）、`concurrent.futures`（多线程）、`queue`（任务队列）
- **开发范式**：模块化设计、队列通信、多线程协作


## 项目结构 📂

```
image-to-video-generator/
├── constants/
│   └── constants.py          # 配置常量（路径、线程数、API密钥、提示词等）
├── inputPic/                 # 默认图片输入文件夹（可在constants中修改路径）
├── outputVideo/              # 默认视频输出文件夹（可在constants中修改路径）
├── utils/
│   ├── image_util.py         # 图片工具类（Base64转换、图片读取、源图删除）
│   └── video_generate.py     # 视频生成类（AI客户端创建、任务提交、状态查询、视频下载）
├── workers/
│   └── processor.py          # 任务处理类（图片处理逻辑、结果队列管理）
├── main.py                   # 程序入口（流程调度、线程管理、总控逻辑）
└── requirements.txt          # 项目依赖清单
```


## 快速开始 🏃

### 前置准备

1. **环境依赖**：安装Python 3.8及以上版本，执行以下命令安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

2. **API密钥配置**：
   - 从[智谱AI开放平台](https://open.bigmodel.cn/)获取API密钥（需开通CogVideoX-Flash模型使用权限）；
   - 设置环境变量：
     ```bash
     # Windows系统（命令提示符）
     set API_KEY=你的智谱AI API密钥
     
     # Linux/Mac系统（终端）
     export API_KEY=你的智谱AI API密钥
     ```

3. **图片准备**：将需要处理的图片放入`inputPic`文件夹（或在`constants.py`中修改`DEFAULT_INPUT_FOLDER`指定自定义路径）。


### 运行步骤

1. 克隆本项目到本地：
   ```bash
   git clone https://github.com/你的用户名/image-to-video-generator.git
   cd image-to-video-generator
   ```

2. （可选）修改配置参数：根据需求调整`constants.py`中的参数，例如：
   - 修改`PROMPT`调整视频动态效果（如“人物自然走动”“镜头环绕物体”）；
   - 修改`THREAD_NUM`调整并行线程数（建议3-5，根据API并发限制调整）；
   - 修改`size`和`fps`调整视频分辨率（如“3840x2160”）和帧率（30/60）。

3. 启动程序：
   ```bash
   python main.py
   ```

4. 查看结果：生成的视频将自动保存到`outputVideo`文件夹，程序运行日志会实时显示处理进度及结果。


## 核心参数配置 ⚙️

| 参数名               | 说明                                  | 可选值/示例                          |
|----------------------|---------------------------------------|-------------------------------------|
| DEFAULT_INPUT_FOLDER | 图片输入文件夹路径                    | "D:\\inputPic" 或 "/home/inputPic"  |
| DEFAULT_OUTPUT_FOLDER| 视频输出文件夹路径                    | "D:\\outputVideo" 或 "/home/outputVideo" |
| THREAD_NUM           | 并行处理线程数                        | 3（根据CPU和API并发限制调整）        |
| PROMPT               | 视频生成提示词（控制动态效果）        | "让人物飞起来"、"人物自然走动"       |
| quality              | 视频生成模式（在video_generate.py中） | "quality"（质量优先）、"speed"（速度优先） |
| size                 | 视频分辨率（在video_generate.py中）   | "1080x1920"、"3840x2160"（4K）      |
| fps                  | 视频帧率（在video_generate.py中）     | 30、60                              |


## 注意事项 ⚠️

1. **API权限**：确保API密钥拥有CogVideoX-Flash模型的调用权限，否则会导致任务提交失败；
2. **网络稳定性**：视频生成和下载依赖网络连接，建议在稳定网络环境下运行；
3. **资源消耗**：高分辨率（如4K）和高帧率（60fps）会增加生成耗时和API资源消耗，需合理选择；
4. **源图清理**：程序默认在图片成功提交任务后删除源文件（避免重复处理），若需保留可注释`image_util.delete_image`调用。


## 贡献与支持 🌟

如果本项目对您的开发工作或学习有帮助，欢迎：
- 点亮GitHub仓库的⭐️ Star，帮助更多开发者发现本项目；
- 提交Issue反馈问题或需求，或通过Pull Request参与功能优化；
- 关注项目更新，后续将支持错误重试、音频生成、自定义水印等扩展功能。

您的支持是项目持续迭代的重要动力！
