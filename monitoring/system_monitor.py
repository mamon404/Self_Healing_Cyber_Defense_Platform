# monitoring/system_monitor.py
import psutil

def get_system_metrics():
    """
    return small dict of system metrics (cpu + memory)
    """
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    return {
        "cpu_percent": cpu,
        "memory_percent": mem
    }

if __name__ == "__main__":
    print(get_system_metrics())

