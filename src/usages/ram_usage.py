import cpuinfo
import psutil
import time

from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class RamInfo:
    total_ram_gb: float
    used_ram_gb: float
    available_ram_gb: float
    ram_percentage: float
    top_ram_processes: list[dict[str, Any]]
