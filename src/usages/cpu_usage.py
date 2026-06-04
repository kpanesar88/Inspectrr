import cpuinfo
import psutil
import time

from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class CpuInfo:
    name: str
    architecture: str
    usage_percentage: float
    cores: int
    threads: int
    curr_freq: Optional[float]
    max_freq: Optional[float]
    max_freq_ghz: Optional[float]
    advertised_hz: Optional[str]
    per_core: list[float]
    top_processes: list[dict[str, Any]]
    datetime: str


def getCpuInfo() -> CpuInfo:
    cpu_details = cpuinfo.get_cpu_info()
    freq = psutil.cpu_freq()

    curr_freq = freq.current if freq else None
    max_freq = freq.max if freq else None
    max_freq_ghz = round(max_freq / 1000, 2) if max_freq else None

    return CpuInfo(
        name=cpu_details.get("brand_raw", "CPU name unavailable"),
        architecture=cpu_details.get("arch", "Architecture unavailable"),
        usage_percentage=psutil.cpu_percent(interval=1),
        cores=psutil.cpu_count(logical=False) or 0,
        threads=psutil.cpu_count(logical=True) or 0,
        curr_freq=curr_freq,
        max_freq=max_freq,
        max_freq_ghz=max_freq_ghz,
        advertised_hz=cpu_details.get("hz_advertised_friendly"),
        per_core=psutil.cpu_percent(interval=0.1, percpu=True),
        top_processes=getTopProcesses(),
        datetime=str(datetime.now())
    )


def getTopProcesses(limit=5):
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    time.sleep(0.5)

    processes_list = []

    for proc in psutil.process_iter():
        try:
            with proc.oneshot():
                pid = proc.pid
                name = proc.name()
                cpu = proc.cpu_percent(interval=None)

                processes_list.append({
                    "pid": pid,
                    "name": name,
                    "cpu_percent": cpu
                })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_processes = sorted(
        processes_list,
        key=lambda x: x["cpu_percent"],
        reverse=True
    )

    return top_processes[:limit]