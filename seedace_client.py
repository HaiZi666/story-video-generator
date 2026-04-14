"""
豆包 SeedAce 2.0 视频生成客户端

API 文档：https://www.volcengine.com/docs/82379/2291680
注意：以下 API 调用格式为参考写法，具体格式需根据官方文档调整
"""

import requests
import time
import os
from typing import Optional
from config import (
    SEEDACE_API_KEY,
    SEEDACE_BASE_URL,
    SEEDACE_MODEL,
    VIDEO_DURATION,
    VIDEO_RESOLUTION,
    VIDEO_ASPECT_RATIO,
    VIDEO_SUBMIT_TIMEOUT,
    VIDEO_POLL_INTERVAL,
    VIDEO_TOTAL_TIMEOUT,
)


class SeedAceClient:
    """豆包 SeedAce 2.0 API 客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or SEEDACE_API_KEY
        self.base_url = base_url or SEEDACE_BASE_URL
        self.model = SEEDACE_MODEL

    def _build_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _submit_task(self, prompt: str) -> str:
        """
        提交视频生成任务

        Args:
            prompt: 视频描述文本（故事内容）

        Returns:
            task_id: 任务 ID，用于后续查询

        Raises:
            Exception: 提交失败时抛出
        """
        if not self.api_key:
            raise ValueError("SEEDACE_API_KEY 未配置，请检查 .env 文件")

        url = f"{self.base_url}/videos/generate"
        headers = self._build_headers()

        payload = {
            "model": self.model,
            "input": {
                "prompt": prompt,
            },
            "parameters": {
                "duration": VIDEO_DURATION,
                "resolution": VIDEO_RESOLUTION,
                "aspect_ratio": VIDEO_ASPECT_RATIO,
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=VIDEO_SUBMIT_TIMEOUT
        )
        response.raise_for_status()

        result = response.json()
        # 根据实际返回格式调整 task_id 字段
        task_id = result.get("task_id") or result.get("id")
        if not task_id:
            raise Exception(f"未找到 task_id，返回内容：{result}")

        print(f"  视频任务已提交，task_id: {task_id}")
        return task_id

    def _poll_task_status(self, task_id: str) -> dict:
        """
        轮询任务状态

        Args:
            task_id: 任务 ID

        Returns:
            任务状态结果（包含 output.video_url）
        """
        url = f"{self.base_url}/videos/tasks/{task_id}"
        headers = self._build_headers()

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def _download_video(self, video_url: str, output_path: str) -> str:
        """
        下载视频到本地

        Args:
            video_url: 视频下载地址
            output_path: 本地保存路径

        Returns:
            本地文件路径
        """
        response = requests.get(video_url, timeout=VIDEO_TOTAL_TIMEOUT, stream=True)
        response.raise_for_status()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return output_path

    def generate_video(
        self,
        story_text: str,
        output_path: str,
        retry: int = 1,
    ) -> str:
        """
        生成视频的完整流程：
        1. 提交生成任务
        2. 轮询等待完成
        3. 下载视频到本地

        Args:
            story_text: 故事文本（将作为视频生成 prompt）
            output_path: 视频保存路径
            retry: 失败重试次数

        Returns:
            本地视频文件路径

        Raises:
            Exception: 生成失败时抛出
        """
        last_error = None

        for attempt in range(retry + 1):
            try:
                # Step 1: 提交任务
                print(f"\n[尝试 {attempt + 1}/{retry + 1}] 提交视频生成任务...")
                task_id = self._submit_task(story_text)

                # Step 2: 轮询等待
                print(f"开始轮询任务状态（间隔 {VIDEO_POLL_INTERVAL} 秒）...")
                elapsed = 0

                while elapsed < VIDEO_TOTAL_TIMEOUT:
                    status_result = self._poll_task_status(task_id)
                    status = status_result.get("status", "pending")

                    if status == "completed":
                        print(f"  视频生成完成！")
                        video_url = status_result.get("output", {}).get("video_url")
                        if not video_url:
                            raise Exception(f"生成完成但未找到 video_url，返回：{status_result}")

                        # Step 3: 下载视频
                        print(f"正在下载视频到：{output_path}")
                        self._download_video(video_url, output_path)
                        return output_path

                    elif status == "failed":
                        error_msg = status_result.get("error", {}).get("message", "未知错误")
                        raise Exception(f"视频生成失败：{error_msg}")

                    elif status == "processing":
                        print(f"  状态：处理中...（已等待 {elapsed} 秒）")

                    else:
                        print(f"  状态：{status}（已等待 {elapsed} 秒）")

                    time.sleep(VIDEO_POLL_INTERVAL)
                    elapsed += VIDEO_POLL_INTERVAL

                # 超时
                raise TimeoutError(f"视频生成超时（已等待 {elapsed} 秒）")

            except Exception as e:
                last_error = e
                print(f"  错误：{e}")

                if attempt < retry:
                    print("  正在重试...")

        raise last_error


# 便捷函数
def generate_video(story_text: str, output_path: str) -> str:
    """生成视频的便捷函数"""
    client = SeedAceClient()
    return client.generate_video(story_text, output_path)


if __name__ == "__main__":
    # 简单测试（需要先配置 .env）
    import os
    from dotenv import load_dotenv
    load_dotenv()

    if not os.getenv("SEEDACE_API_KEY"):
        print("请先在 .env 中配置 SEEDACE_API_KEY")
    else:
        test_prompt = "一个小男孩在阳光下追逐蝴蝶，蝴蝶飞过彩虹桥消失了。"
        print(f"测试 prompt：{test_prompt}")
        print("-" * 40)
        try:
            output = "output/test_video.mp4"
            result = generate_video(test_prompt, output)
            print(f"视频生成成功：{result}")
        except Exception as e:
            print(f"视频生成失败：{e}")
