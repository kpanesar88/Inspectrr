import cpuinfo
import psutil
import time

from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class RamInfo:
    total_ram_mb: float
    total_ram_gb: float
    used_ram_mb: float
    used_ram_gb: float
    available_ram_mb: float
    available_ram_gb: float
    ram_percentage: float
    top_ram_processes: list[dict[str, Any]]
    ram_state: str



def getRamInfo() -> RamInfo:
    
    ram = psutil.virtual_memory()
       
    ram_percent = ram.percent
    
    getTopRamProcesses()
    getRamState(ram_percent=ram.percent)
    
    return RamInfo(
        total_ram_mb = ram.total,
        total_ram_gb = ram.total / (1024**3),
        used_ram_mb = ram.used,
        used_ram_gb = ram.used / (1024**3),
        available_ram_mb = ram.available,
        available_ram_gb = ram.available / (1024**3),
        ram_percentage = ram.percent,
        top_ram_processes= getTopRamProcesses(limit=5),
        ram_state = getRamState(ram.percent),
        
    )
    
    
    
def getRamState(ram_percent):
    
    if ram_percent is None:
        return "Unavailable"
    
    if ram_percent < 10:
        return "Idle"
    elif ram_percent >= 85:
        return "High Load"
    elif ram_percent >= 65:
        return "Moderate Load"
    else:
        return "Normal"
    

def getTopRamProcesses(limit=5):
    
    top_ram_processes = []
    
    for proc in psutil.process_iter(['pid','name','memory_info']):
        
        try: 
            ram_bytes = proc.info['memory_info'].rss
            ram_mb = ram_bytes / (1024 * 1024)
            
            top_ram_processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'ram_mb': ram_mb
            })
            
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        
    top_ram_processes.sort(key=lambda x: x['ram_mb'], reverse = True)
    
    return top_ram_processes[:limit]