import uvicorn
from fastapi import FastAPI,Request
from root_agent import agent

app = FastAPI()

@app.post("/agent")
async def run_agent(request: Request):
    data = await request.json()
    text = data.get("request", "")
    return await agent.call_agent_async(text)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)