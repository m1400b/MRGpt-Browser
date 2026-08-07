"""
MRGpt Browser

VPN Configuration Model
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.entity_model import EntityModel


@dataclass(slots=True)
class VPNConfig(EntityModel):
    """
    VPN / Proxy Configuration
    """

    # -------------------------------------------------
    # Basic Information
    # -------------------------------------------------

    name: str = ""

    protocol: str = ""

    enabled: bool = True

    auto_connect: bool = False

    # -------------------------------------------------
    # Server
    # -------------------------------------------------

    server: str = ""

    port: int = 0

    country: str = ""

    city: str = ""

    remark: str = ""

    # -------------------------------------------------
    # Authentication
    # -------------------------------------------------

    username: str = ""

    password: str = ""

    method: str = ""

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    config_path: str = ""

    config_text: str = ""

    uri: str = ""

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------

    latency: int = -1

    upload_speed: float = 0.0

    download_speed: float = 0.0

    ping_success: bool = False

    last_error: str = ""

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    connection_count: int = 0

    favorite: bool = False

    priority: int = 0

    # -------------------------------------------------

    @property
    def address(self) -> str:
        """
        server:port
        """

        if not self.server:

            return ""

        return f"{self.server}:{self.port}"

    # -------------------------------------------------

    @property
    def is_valid(self) -> bool:
        """
        Basic validation.
        """

        return (

            bool(self.server)

            and

            self.port > 0

        )

    # -------------------------------------------------

    def increase_connection(self):

        self.connection_count += 1

        self.touch()

    # -------------------------------------------------

    def reset_statistics(self):

        self.connection_count = 0

        self.latency = -1

        self.upload_speed = 0.0

        self.download_speed = 0.0

        self.ping_success = False

        self.last_error = ""

        self.touch()

    # -------------------------------------------------

    def __str__(self):

        return (

            f"{self.name} "

            f"({self.protocol})"

        )