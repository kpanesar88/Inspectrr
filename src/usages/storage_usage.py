import psutil

from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class StorageInfo:
    drive: str
    file_system: Optional[str]
    total_gb: float
    used_gb: float
    free_gb: float
    usage_percentage: float
    state: str


@dataclass
class StorageReport:
    drives: list[StorageInfo]
    datetime: str


def classifyStorageState(usage_percentage: float) -> str:
    if usage_percentage >= 95:
        return "Critical"

    elif usage_percentage >= 85:
        return "Low Space"

    elif usage_percentage >= 70:
        return "Getting Full"

    else:
        return "Healthy"


def bytesToGb(bytes_value: int) -> float:
    return round(bytes_value / (1024 ** 3), 2)


def getStorageInfo() -> StorageReport:
    drives = []

    partitions = psutil.disk_partitions()

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            total_gb = bytesToGb(usage.total)
            used_gb = bytesToGb(usage.used)
            free_gb = bytesToGb(usage.free)
            usage_percentage = usage.percent

            storage_state = classifyStorageState(usage_percentage)

            drives.append(
                StorageInfo(
                    drive=partition.mountpoint,
                    file_system=partition.fstype,
                    total_gb=total_gb,
                    used_gb=used_gb,
                    free_gb=free_gb,
                    usage_percentage=usage_percentage,
                    state=storage_state
                )
            )

        except PermissionError:
            continue

        except Exception:
            continue

    return StorageReport(
        drives=drives,
        datetime=str(datetime.now())
    )