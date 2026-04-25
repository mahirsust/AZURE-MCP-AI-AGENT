from fastapi import FastAPI
from agent.agent import run_agent
from dotenv import load_dotenv
from schema.agent import QueryRequest

load_dotenv()

app = FastAPI(title="AI Agent MCP Platform", version="1.0")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-agent-running"
    }

@app.post("/agent/query")
def agent_query(req: QueryRequest):
    return run_agent(req.query)

@app.get("/agent/demo")
def demo():
    return run_agent("generate operations report")