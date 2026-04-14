#!/usr/bin/env python3
"""
课前故事视频生成器 - MVP 主程序

功能：
1. 输入知识点
2. 调用 MiniMax 生成故事
3. 调用豆包 SeedAce 2.0 生成视频

用法：
    python story_video_generator.py
"""

import os
import sys
import uuid
from datetime import datetime
from typing import Optional

from config import (
    OUTPUT_DIR,
    STORIES_DIR,
    VIDEOS_DIR,
    HISTORICAL_STORY_PROMPT_TEMPLATE,
)
from minimax_client import MiniMaxClient, generate_story as gen_story
from seedace_client import SeedAceClient, generate_video as gen_video


def print_banner():
    """打印欢迎 banner"""
    banner = """
╔══════════════════════════════════════════════════════╗
║         📖 课前故事视频生成器 - MVP                  ║
║                                                      ║
║  知识点 → AI 故事 → AI 视频                          ║
║                                                      ║
║  故事类型：                                           ║
║    1️⃣ 普通故事 - 根据知识点生成趣味小故事            ║
║    2️⃣ 历史故事·趣事 - 搜索历史典故，引出知识点       ║
╚══════════════════════════════════════════════════════╝
    """
    print(banner)


def ensure_dirs():
    """确保输出目录存在"""
    os.makedirs(STORIES_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)


def select_story_type() -> str:
    """选择故事类型"""
    print("\n📝 请选择故事类型：")
    print("   1 - 普通故事（根据知识点生成趣味小故事）")
    print("   2 - 历史故事·趣事（搜索历史典故，引出知识点）")
    print()

    while True:
        choice = input("请输入选项（1 或 2）: ").strip()
        if choice == "1":
            return "normal"
        elif choice == "2":
            return "historical"
        else:
            print("⚠️  无效选项，请输入 1 或 2")


def input_knowledge_point(story_type: str) -> str:
    """获取知识点输入"""
    if story_type == "historical":
        print("\n📝 请输入知识点描述（按回车结束）：")
        print("   （例如：光的折射——为什么筷子放在水里看起来像折断了？）")
        print("   （系统将搜索相关的历史典故、趣事来引出知识点）")
    else:
        print("\n📝 请输入知识点描述（按回车结束）：")
        print("   （例如：光的折射——为什么筷子放在水里看起来像折断了？）")
    print()

    knowledge_point = input("> ").strip()

    while not knowledge_point:
        print("⚠️  知识点不能为空，请重新输入：")
        knowledge_point = input("> ").strip()

    return knowledge_point


def generate_and_save_story(knowledge_point: str, story_type: str = "normal") -> tuple[str, str]:
    """
    生成故事并保存

    Args:
        knowledge_point: 知识点
        story_type: 故事类型，"normal" 或 "historical"

    Returns:
        (story_text, story_path)
    """
    if story_type == "historical":
        print("\n🔍 正在搜索历史典故...")
        print("\n🤖 正在调用 MiniMax 整理历史故事...")
        print("   （预计 10-30 秒，请耐心等待...）\n")
        prompt_template = HISTORICAL_STORY_PROMPT_TEMPLATE
    else:
        print("\n🤖 正在调用 MiniMax 生成故事...")
        print("   （预计 10-30 秒，请耐心等待...）\n")
        prompt_template = STORY_PROMPT_TEMPLATE

    try:
        from minimax_client import generate_story as gen_story
        story = gen_story(knowledge_point, prompt_template)
    except Exception as e:
        print(f"\n❌ 故事生成失败：{e}")
        sys.exit(1)

    # 保存故事文本
    story_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = "historical" if story_type == "historical" else "story"
    story_path = os.path.join(
        STORIES_DIR,
        f"{prefix}_{timestamp}_{story_id}.txt"
    )

    os.makedirs(STORIES_DIR, exist_ok=True)

    story_type_label = "历史故事·趣事" if story_type == "historical" else "普通故事"
    with open(story_path, "w", encoding="utf-8") as f:
        f.write(f"知识点：{knowledge_point}\n")
        f.write(f"故事类型：{story_type_label}\n")
        f.write(f"生成时间：{datetime.now()}\n")
        f.write(f"故事ID：{story_id}\n")
        f.write("=" * 50 + "\n\n")
        f.write("【故事内容】\n\n")
        f.write(story)

    print("✅ 故事生成成功！")
    print(f"   已保存至：{story_path}\n")

    return story, story_path


def print_story(story: str):
    """打印故事内容"""
    print("=" * 50)
    print("【生成的故事】")
    print("=" * 50)
    print(story)
    print("=" * 50)


def confirm_video_generation() -> bool:
    """询问是否生成视频"""
    print("\n是否生成视频？")
    print("  输入 y 或回车：确认生成")
    print("  输入 n：跳过视频生成")
    print("  输入其他：重新生成故事")

    choice = input("> ").strip().lower()

    if choice == "y" or choice == "":
        return True
    elif choice == "n":
        return False
    else:
        return None  # 表示重新生成


def generate_video_output_path(story_id: str) -> str:
    """生成视频输出路径"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}_{story_id}.mp4"
    return os.path.join(VIDEOS_DIR, filename)


def do_generate_video(story: str, story_id: str) -> Optional[str]:
    """
    执行视频生成

    Returns:
        video_path 或 None（如果跳过/失败）
    """
    video_path = generate_video_output_path(story_id)

    print("\n🎬 正在调用豆包 SeedAce 2.0 生成视频...")
    print("   （预计 1-3 分钟，请耐心等待...）")
    print("   （视频生成过程中请勿关闭程序）\n")

    try:
        client = SeedAceClient()
        result_path = client.generate_video(story, video_path)
        print(f"\n✅ 视频生成成功！")
        print(f"   视频保存至：{result_path}")
        return result_path

    except TimeoutError as e:
        print(f"\n⚠️  视频生成超时：{e}")
        print("   建议：尝试缩短故事文本后重新生成")
        return None

    except Exception as e:
        print(f"\n❌ 视频生成失败：{e}")
        return None


def main():
    """主流程"""
    print_banner()
    ensure_dirs()

    # Step 1: 选择故事类型
    story_type = select_story_type()

    # Step 2: 输入知识点
    knowledge_point = input_knowledge_point(story_type)

    # Step 3: 生成故事
    story, story_path = generate_and_save_story(knowledge_point, story_type)

    # Step 4: 展示故事并确认
    while True:
        print_story(story)

        confirm = confirm_video_generation()

        if confirm is None:
            # 重新生成故事
            print("\n🔄 重新生成故事...")
            story, story_path = generate_and_save_story(knowledge_point, story_type)
            continue

        if not confirm:
            # 跳过
            print("\n已跳过视频生成")
            print(f"\n📝 故事文本已保存：{story_path}")
            print("\n感谢使用！👋")
            return

        # 确认生成视频
        # 提取 story_id 从路径
        story_id = os.path.basename(story_path).replace("story_", "").replace("historical_", "").replace(".txt", "").split("_")[-1]
        video_path = do_generate_video(story, story_id)

        if video_path:
            print("\n" + "=" * 50)
            print("🎉 全部完成！")
            print("=" * 50)
            print(f"\n📝 故事文本：{story_path}")
            print(f"🎬 视频文件：{video_path}")
        else:
            print("\n⚠️  视频生成未成功，可稍后重试")

        print("\n感谢使用！👋")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断，程序退出")
        sys.exit(0)
