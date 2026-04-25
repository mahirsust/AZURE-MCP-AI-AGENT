import requests
import os
from openai import AzureOpenAI
from agent.tools_schema import tools

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

MCP_BASE = os.getenv("MCP_BASE_URL")


def call_tool(name):

    if name == "get_orders":
        return requests.get(f"{MCP_BASE}/orders").json()

    if name == "get_inventory":
        return requests.get(f"{MCP_BASE}/inventory").json()

    if name == "detect_anomalies":
        return requests.get(f"{MCP_BASE}/anomalies").json()

    if name == "generate_report":

        orders = call_tool("get_orders")
        inventory = call_tool("get_inventory")
        anomalies = call_tool("detect_anomalies")

        return {
            "orders": orders,
            "inventory": inventory,
            "anomalies": anomalies
        }


def run_agent(query):

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are an enterprise operations AI agent."},
            {"role": "user", "content": query}
        ],
        tools=tools,
        tool_choice="auto"
    )

    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        tool_name = tool_calls[0].function.name
        result = call_tool(tool_name)

        return {
            "tool_used": tool_name,
            "result": result
        }

    return {"message": "No tool selected"}