from abc import ABC, abstractmethod


class AbstractLogin(ABC):
    """浏览器模式平台的登录抽象。首期仅定义接口，不提供具体平台实现。"""

    @abstractmethod
    async def begin(self) -> None:
        """登录入口：按配置的 LOGIN_TYPE 分派到具体登录方式。"""
        raise NotImplementedError

    @abstractmethod
    async def login_by_qrcode(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def login_by_cookie(self) -> None:
        raise NotImplementedError
