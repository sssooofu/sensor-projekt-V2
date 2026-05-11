import os

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8080))
DB_PATH = os.environ.get("DB_PATH", "sensor_hub.db")
DASHBOARD_DIR = os.environ.get(
    "DASHBOARD_DIR",
    os.path.join(os.path.dirname(__file__), "..", "..", "dashboard")
)
