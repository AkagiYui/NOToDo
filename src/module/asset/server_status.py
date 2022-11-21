from dataclasses import dataclass


@dataclass
class ServerStatus:
    """服务器状态"""

    python_version: str
    system_description: str

    system_cpu_present: float
    system_memory_usage: float
    script_memory_usage: float

    system_uptime: str
    script_uptime: str

    app_name: str
    version: str
