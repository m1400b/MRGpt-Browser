"""
MRGpt Browser

Service Container
"""

from __future__ import annotations

from typing import Any


class ServiceContainer:
    """
    Dependency Injection Container

    تمامی سرویس‌های پروژه از طریق این کلاس
    ثبت و دریافت می‌شوند.
    """

    def __init__(self) -> None:

        self._services: dict[str, Any] = {}

    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        service: Any
    ) -> None:
        """
        Register a service instance.
        """

        if name in self._services:
            raise KeyError(
                f'Service "{name}" already registered.'
            )

        self._services[name] = service

    # ---------------------------------------------------------

    def replace(
        self,
        name: str,
        service: Any
    ) -> None:
        """
        Replace an existing service.
        """

        self._services[name] = service

    # ---------------------------------------------------------

    def resolve(
        self,
        name: str
    ) -> Any:
        """
        Resolve a service.
        """

        if name not in self._services:
            raise KeyError(
                f'Service "{name}" not found.'
            )

        return self._services[name]

    # ---------------------------------------------------------

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self._services

    # ---------------------------------------------------------

    def unregister(
        self,
        name: str
    ) -> None:

        self._services.pop(name, None)

    # ---------------------------------------------------------

    def clear(self) -> None:

        self._services.clear()

    # ---------------------------------------------------------

    @property
    def services(self) -> dict[str, Any]:

        return self._services.copy()

    # ---------------------------------------------------------

    def __contains__(
        self,
        name: str
    ) -> bool:

        return name in self._services

    # ---------------------------------------------------------

    def __getitem__(
        self,
        name: str
    ) -> Any:

        return self.resolve(name)

    # ---------------------------------------------------------

    def __setitem__(
        self,
        name: str,
        service: Any
    ) -> None:

        self.register(name, service)
    
    def get(
    self,
    name: str,
) -> Any:

        return self.resolve(name)


    def set(
        self,
        name: str,
        service: Any,
    ) -> None:

        self.register(
            name,
            service,
        )
    
    def shutdown(self) -> None:

        for service in self._services.values():
        
            shutdown = getattr(
                service,
                "shutdown",
                None,
            )
    
            if callable(shutdown):
            
                shutdown()
    
        self.clear()