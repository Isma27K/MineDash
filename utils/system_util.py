import time

import psutil

cpu_percent = psutil.cpu_percent(interval=1)

mem = psutil.virtual_memory()

total_ram = f"{mem.total / (1024 ** 3): .2f}"
available_ram = f"{mem.available / (1024 ** 3): .2f}"
used_ram = f"{mem.used / (1024 ** 3): .2f}"
used_ram_percent = f"{mem.percent}"


# Get initial disk I/O
disk1 = psutil.disk_io_counters()
time.sleep(1)
# Get disk I/O after 1 second
disk2 = psutil.disk_io_counters()

# Calculate bytes read and written during 1 second
read_bytes = disk2.read_bytes - disk1.read_bytes
write_bytes = disk2.write_bytes - disk1.write_bytes

# Average I/O (Read + Write) in bytes/sec
avg_io_bytes = (read_bytes + write_bytes)

# Convert to KB/sec or MB/sec for readability
avg_io_kb = avg_io_bytes / 1024
avg_io_mb = f"{avg_io_bytes / (1024 ** 2) : .2f}"
