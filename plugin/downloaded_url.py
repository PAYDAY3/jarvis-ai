
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from plugin.plugin_interface import AbstractPlugin, PluginResult
from jarvis.jarvis import takecommand
from my_package import Logging

TEMP_DIR_PATH = "./temp"

logger = Logging.getLogger(__name__)

class DownloadURLPlugin(AbstractPlugin):
    def valid(self) -> bool:
        return True

    def __init__(self):
        self._logger = None

    def init(self, logging):
        self.logger = Logging.getLogger(self.name)

    def get_name(self):
        return "download_url"

    def get_chinese_name(self):
        return "下载网页"

    def get_description(self):
        return "下载网页接口，当你需要下载某个url的内容时，你应该调用本接口。\n" \
               "当我的输入内容是一个网页url时，你应该优先考虑调用本接口下载网页内容，然后再对网页内容进行下一步的处理，以满足我的需求。"

    def get_parameters(self):
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "要下载的网页url",
                }
            },
            "required": ["url"],
        }

    def run(self, takecommand: str, args: dict) -> PluginResult:
        urt = args.get("url")
        if not url:
            return PluginResult.new(
                result=None, need_call_brain=False, success=False, 
                error_message="缺少url参数"
            )

        try:
            # 使用 requests 下载网页内容
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            # 将内容保存到文件中
            file_name = f"download_url-{int(time.time())}.txt"
            file_path = os.path.abspath(os.path.join(system_config.TEMP_DIR_PATH, file_name))
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_content)
            
            self.logger.info(f"网页内容已下载并保存到 {file_path}")

            return PluginResult.new(
                result=f"我已将该网页的内容下载到文件【{file_path}】中。你应该优先考虑使用【文档问答】接口直接进行特定问题的问答。",
                need_call_brain=True,
                success=True
            )
        except requests.RequestException as e:
            self.logger.error(f"下载网页时出错: {str(e)}")
            return PluginResult.new(
            result=None, need_call_brain=False, success=False, 
            error_message=f"下载网页时出错: {str(e)}"
        )

        except Exception as e:
            self.logger.error(f"处理网页时出错: {str(e)}")
            return PluginResult.new(
            result=None, need_call_brain=False, success=False, 
            error_message=f"处理网页时出错: {str(e)}"    
            )