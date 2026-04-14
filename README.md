# 📖 课前故事视频生成器 - MVP

基于 AI 的课前故事视频生成工具：将知识点转换为趣味故事，并生成配套短视频。

## 功能特性

- ✅ 输入知识点，AI 生成课前小故事（MiniMax 大模型）
- ✅ 将故事转化为短视频（豆包 SeedAce 2.0）
- ✅ 支持视频预览和本地下载
- ⏳ 更多功能（经典故事匹配、Web界面等）开发中

## 系统要求

- Python 3.10+
- MiniMax API Key（火山引擎开放平台）
- 豆包 SeedAce 2.0 API Key（火山引擎开放平台）

## 安装

```bash
# 1. 进入项目目录
cd story-video-mvp

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API Key
cp .env.example .env
# 编辑 .env，填入实际 API Key
```

## 使用方法

```bash
# 运行程序
python story_video_generator.py
```

### 使用流程

```
1. 运行程序，输入知识点描述
2. 等待 MiniMax 生成故事（10-30秒）
3. 查看生成的故事，可选择重新生成或继续
4. 确认后开始生成视频（1-3分钟）
5. 视频生成完成，自动保存到 output/videos/
```

### 输出文件

- 故事文本：`output/stories/story_YYYYMMDD_HHMMSS_xxxxxxxx.txt`
- 视频文件：`output/videos/video_YYYYMMDD_HHMMSS_xxxxxxxx.mp4`

## 项目结构

```
story-video-mvp/
├── story_video_generator.py   # 主程序入口
├── minimax_client.py          # MiniMax API 客户端
├── seedace_client.py          # 豆包 SeedAce 2.0 客户端
├── config.py                  # 配置管理
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量示例
├── README.md                  # 说明文档
└── output/                    # 输出目录
    ├── stories/               # 故事文本
    └── videos/               # 视频文件
```

## 配置说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `MINIMAX_API_KEY` | MiniMax API Key | - |
| `SEEDACE_API_KEY` | 豆包 SeedAce API Key | - |
| `VIDEO_DURATION` | 视频最大时长（秒） | 60 |
| `VIDEO_RESOLUTION` | 视频分辨率 | 720p |
| `STORY_TIMEOUT` | 故事生成超时（秒） | 30 |
| `VIDEO_TOTAL_TIMEOUT` | 视频生成总超时（秒） | 300 |

## API 文档

- MiniMax：https://www.minimax.chat/
- 火山引擎（SeedAce）：https://www.volcengine.com/docs/82379/2291680

## 常见问题

**Q: 视频生成需要多长时间？**
A: 通常 1-3 分钟，取决于服务器负载和视频长度。

**Q: 视频生成失败怎么办？**
A: 检查 API Key 是否正确，网络是否稳定，或尝试缩短故事文本后重试。

**Q: 如何修改视频风格？**
A: 目前 MVP 版本暂不支持视频风格选择，后续版本将支持。

## License

MIT
