"""
配置管理 - 课前故事视频生成器 MVP
所有配置通过环境变量读取，参考 .env.example
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件（如果存在）
load_dotenv()


# ============ MiniMax 配置 ============
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")

# MiniMax 模型名称（根据实际申请到的模型填写）
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "MiniMax-Text-01")

# ============ 豆包 SeedAce 2.0 配置 ============
SEEDACE_API_KEY = os.getenv("SEEDACE_API_KEY", "")
SEEDACE_BASE_URL = os.getenv("SEEDACE_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")

# SeedAce 模型名称
SEEDACE_MODEL = os.getenv("SEEDACE_MODEL", "seedance-2.0")

# ============ 视频参数 ============
VIDEO_DURATION = int(os.getenv("VIDEO_DURATION", "60"))  # 最大 60 秒
VIDEO_RESOLUTION = os.getenv("VIDEO_RESOLUTION", "720p")
VIDEO_ASPECT_RATIO = os.getenv("VIDEO_ASPECT_RATIO", "16:9")

# ============ 超时设置 ============
STORY_TIMEOUT = int(os.getenv("STORY_TIMEOUT", "30"))     # 故事生成超时（秒）
VIDEO_SUBMIT_TIMEOUT = int(os.getenv("VIDEO_SUBMIT_TIMEOUT", "30"))  # 视频提交请求超时
VIDEO_POLL_INTERVAL = int(os.getenv("VIDEO_POLL_INTERVAL", "5"))    # 轮询间隔（秒）
VIDEO_TOTAL_TIMEOUT = int(os.getenv("VIDEO_TOTAL_TIMEOUT", "300"))  # 视频生成总超时

# ============ Prompt 配置 ============
STORY_PROMPT_TEMPLATE = """请根据以下知识点生成一个适合课前讲述的小故事，时长约15秒-1分钟（150-500字），故事要有趣味性，能引发学生学习兴趣。

知识点：{knowledge_point}

请直接输出故事内容，不要其他说明。"""

# ============ 历史故事·趣事模块 Prompt ============
HISTORICAL_STORY_PROMPT_TEMPLATE = """你是一位历史故事专家。请根据以下知识点，搜索相关的历史典故、历史故事或趣味史料，并整理成一个完整的、有趣的历史故事。

【要求】
1. 先搜索/回忆该知识点相关的历史典故、名人轶事、历史事件等
2. 如果找到合适的历史故事，将其整理成完整的故事情节
3. 故事要生动有趣，适合课前讲述（3-5分钟，400-800字）
4. 故事结尾要自然引出知识点，激发学生学习兴趣
5. 可以加入对话、心理描写，让故事更生动
6. 如果确实没有相关的历史典故，可以创作一个符合历史背景的趣味故事

知识点：{knowledge_point}

请按以下格式输出：
【历史典故】（如果没有合适的，写"原创故事"）
典故名称/来源：xxx

【故事正文】
（完整的故事情节）

【知识点引入】
（故事如何引出本课知识点）"""

# ============ 目录配置 ============
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
STORIES_DIR = os.path.join(OUTPUT_DIR, "stories")
VIDEOS_DIR = os.path.join(OUTPUT_DIR, "videos")
