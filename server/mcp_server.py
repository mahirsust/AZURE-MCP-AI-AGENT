from fastapi import FastAPI
from tools.orders import get_orders
from tools.inventory import get_inventory
from tools.anomaly import detect_anomalies

app = FastAPI(title="MCP Tool Server")

@app.get("/orders")
def orders():
    return get_orders()

@app.get("/inventory")
def inventory():
    return get_inventory()

@app.get("/anomalies")
def anomalies():
    return detect_anomalies()