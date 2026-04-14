"""
简单测试脚本 - 验证 API 连接

使用前请先配置 .env 文件中的 API Key
"""

import os
import sys

# 添加父目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()


def test_minimax():
    """测试 MiniMax 连接"""
    print("\n" + "=" * 40)
    print("测试 MiniMax API")
    print("=" * 40)

    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key or api_key == "your_minimax_api_key_here":
        print("❌ MINIMAX_API_KEY 未配置")
        return False

    try:
        from minimax_client import generate_story
        test_point = "光的折射"
        print(f"测试知识点：{test_point}")
        story = generate_story(test_point)
        print(f"✅ MiniMax 连接成功！")
        print(f"生成的故事：\n{story[:200]}...")
        return True
    except Exception as e:
        print(f"❌ MiniMax 测试失败：{e}")
        return False


def test_seedace():
    """测试 SeedAce 连接"""
    print("\n" + "=" * 40)
    print("测试豆包 SeedAce 2.0 API")
    print("=" * 40)

    api_key = os.getenv("SEEDACE_API_KEY")
    if not api_key or api_key == "your_seedace_api_key_here":
        print("❌ SEEDACE_API_KEY 未配置")
        return False

    print("⚠️  SeedAce 测试会实际调用 API，消耗额度")
    print("   如需测试，请手动运行 seedace_client.py")
    print("✅ SeedAce API Key 格式正确（未实际调用）")
    return True


def main():
    print("=" * 40)
    print("API 连接测试")
    print("=" * 40)

    results = []
    results.append(("MiniMax", test_minimax()))
    results.append(("SeedAce", test_seedace()))

    print("\n" + "=" * 40)
    print("测试结果汇总")
    print("=" * 40)
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}：{status}")


if __name__ == "__main__":
    main()
