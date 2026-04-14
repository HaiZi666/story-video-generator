"""
MiniMax 大模型客户端 - 故事生成
"""

import requests
from typing import Optional
from config import (
    MINIMAX_API_KEY,
    MINIMAX_BASE_URL,
    MINIMAX_MODEL,
    STORY_TIMEOUT,
    STORY_PROMPT_TEMPLATE,
)


class MiniMaxClient:
    """MiniMax API 客户端"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or MINIMAX_API_KEY
        self.base_url = base_url or MINIMAX_BASE_URL
        self.model = MINIMAX_MODEL

    def _build_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_story(self, knowledge_point: str, prompt_template: str = None, retry: int = 1) -> str:
        """
        调用 MiniMax 大模型生成故事

        Args:
            knowledge_point: 知识点描述
            prompt_template: 自定义 prompt 模板（可选，默认使用 STORY_PROMPT_TEMPLATE）
            retry: 失败重试次数

        Returns:
            故事文本

        Raises:
            Exception: API 调用失败时抛出
        """
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY 未配置，请检查 .env 文件")

        url = f"{self.base_url}/text/chatcompletion_v2"
        headers = self._build_headers()

        if prompt_template is None:
            prompt_template = STORY_PROMPT_TEMPLATE
        prompt = prompt_template.format(knowledge_point=knowledge_point)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }

        last_error = None
        for attempt in range(retry + 1):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=STORY_TIMEOUT
                )
                response.raise_for_status()

                result = response.json()
                # 提取故事文本（根据实际返回格式调整）
                story = result["choices"][0]["message"]["content"]
                return story.strip()

            except requests.exceptions.Timeout:
                last_error = Exception(f"MiniMax API 超时（尝试 {attempt + 1}/{retry + 1}）")
            except requests.exceptions.HTTPError as e:
                last_error = Exception(f"MiniMax API HTTP 错误：{e}\n响应内容：{e.response.text}")
            except Exception as e:
                last_error = Exception(f"MiniMax API 调用失败：{e}")

            if attempt < retry:
                print(f"  警告：{last_error}，重试中...")

        raise last_error


# 便捷函数
def generate_story(knowledge_point: str, prompt_template: str = None) -> str:
    """生成故事的便捷函数"""
    client = MiniMaxClient()
    return client.generate_story(knowledge_point, prompt_template)


if __name__ == "__main__":
    # 简单测试（需要先配置 .env）
    import os
    from dotenv import load_dotenv
    load_dotenv()

    if not os.getenv("MINIMAX_API_KEY"):
        print("请先在 .env 中配置 MINIMAX_API_KEY")
    else:
        test_knowledge = "光的折射：为什么筷子放在水里看起来像折断了？"
        print(f"测试知识点：{test_knowledge}")
        print("-" * 40)
        story = generate_story(test_knowledge)
        print(story)
