import os
import time

from my_package import Logging
from plugin.plugin_interface import AbstractPlugin, PluginResult
from jarvis.jarvis import takecommand

TEMP_DIR_PATH = "./temp"

logger = Logging.getLogger(__name__)

class WriteFilePlugin(AbstractPlugin):
    def valid(self) -> bool:
        return True

    def init(self, logger):
        self.name = "write_file"
        self.chinese_name = "写入文件"
        self.description = "把信息写入文件"

        self._logger = logger

    def get_name(self):
        return "write_file"

    def get_chinese_name(self):
        return "写入文件"

    def get_description(self):
        return "写入文件内容接口，当你需要向一个文件中写入内容时，你应该调用本接口，传入要写入的内容。"

    def get_parameters(self):
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "要写入的内容",
                },
                "encoding": {
                    "type": "string",
                    "description": "文件编码格式，例如 'utf-8', 'utf-16', 等",
                    "default": "utf-8",
                },
            },
            "required": ["content"],
        }

    def run(self, takecommand: str, args: dict) -> PluginResult:
        self._logger.info("开始执行写入文件操作")
        
        if takecommand is None:
            self._logger.warning("没有检测到语音指令")
            return PluginResult.new("没有检测到语音指令", need_call_brain=False)

        content = args.get("content")
        encoding = args.get("encoding", "utf-8")

        if content:
            try:
                os.makedirs(TEMP_DIR_PATH, exist_ok=True)
                file_name = f"写入文件-{str(int(time.time()))}.md"
                file_path = os.path.abspath(os.path.join(TEMP_DIR_PATH, file_name))

                self._logger.info(f"准备将内容写入到文件: {file_path}")
            
                with open(file_path, "w", encoding=encoding) as f:
                    f.write(content)
                self._logger.info(f"内容成功写入文件: {file_path}")
                return PluginResult.new(result=f"已将内容写入到文件【{file_path}】中。", need_call_brain=True)
            except Exception as e:
                self._logger.error(f"写入文件时出错: {str(e)}")
                return PluginResult.new(result=f"写入文件时出错: {str(e)}", need_call_brain=False)
        else:
            self._logger.warning("写入内容不能为空")
            return PluginResult.new(result="写入内容不能为空。", need_call_brain=False)
