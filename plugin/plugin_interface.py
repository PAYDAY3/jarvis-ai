from my_package import Logging
from abc import ABCMeta, abstractmethod
from jarvis.jarvis import takecommand
from datetime import datetime

logging = Logging.getLogger(__name__)

class PluginResult(object):
    def __init__(self):
        # 字符串格式，AI主要参考的结果
        self.result = None
        # 是否需要在执行完成后再次调用大脑处理
        self.need_call_brain = None
        # 错误信息，默认为None，表示没有错误
        self.error_message = None
        # 执行状态，True表示成功，False表示失败
        self.success = True
        # 执行时间（可选）
        self.execution_time = None
        # 插件元数据，如名称、版本等
        self.metadata = {}
        self.status = None
        self.additional_data = None
        self.timestamp = datetime.now()
        
    @staticmethod
    def new(result: str, need_call_brain: bool, success: bool = True, error_message: str = None, 
            execution_time: float = None, metadata: dict = None, status: str = None, additional_data: dict = None):
        r = PluginResult()
        r.result = result
        r.need_call_brain = need_call_brain
        r.success = success
        r.error_message = error_message
        r.execution_time = execution_time
        r.metadata = metadata if metadata else {}
        r.status = status
        r.additional_data = additional_data if additional_data else {}
        r.timestamp = datetime.now()
        return r
        
    def is_success(self):
        return self.success

    def has_error(self):
        return self.error_message is not None

    def add_metadata(self, key: str, value):
        self.metadata[key] = value

    def get_metadata(self, key: str):
        return self.metadata.get(key)

    def __str__(self):
        return (f"PluginResult(result={self.result}, need_call_brain={self.need_call_brain}, "
                f"success={self.success}, error_message={self.error_message}, execution_time={self.execution_time}, "
                f"metadata={self.metadata}, status={self.status}, additional_data={self.additional_data})")

class AbstractPlugin(metaclass=ABCMeta):

    @abstractmethod
    def valid(self) -> bool:
        pass

    @abstractmethod
    def init(self, logging):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_chinese_name(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_parameters(self):
        pass
    @abstractmethod
    def on_startup(self):
        pass

    @abstractmethod
    def on_shutdown(self):
        pass

    @abstractmethod
    def on_pause(self):
        pass

    @abstractmethod
    def on_resume(self):
        pass
        
    @abstractmethod
    def run(self, takecommand: str, args: dict) -> PluginResult:
        pass
