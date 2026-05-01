# detection/run_anomaly_detector.py
import time
from detection.anomaly_detector import AnomalyDetector

def main():
    det = AnomalyDetector(sample_interval=5, window_seconds=60)
    print("[anomaly] starting sampling every 5s")
    try:
        det.run()
    except KeyboardInterrupt:
        print("[anomaly] stopped")

if __name__ == "__main__":
    main()

