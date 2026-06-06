from usages.cpu_usage import getCpuInfo
from usages.ram_usage import getRamInfo
from usages.storage_usage import getStorageInfo

cpu = getCpuInfo()
ram = getRamInfo()
storage = getStorageInfo()
# print(cpu)
# print(ram)
print(storage)