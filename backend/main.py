import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from root_agent import agent
from ag_ui.core import RunAgentInput, TextMessageContentEvent, EventType
from ag_ui.encoder import EventEncoder

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/agent")
async def run_agent(request: Request):
    data = await request.json()
    agent_input = RunAgentInput(**data)
    text = ""
    if agent_input.context:
        first_context = agent_input.context[0]
        value = getattr(first_context, "value", "")
        text = value if isinstance(value, str) else str(value)
    encoder = EventEncoder()
    message_id = str(uuid.uuid4())

    async def event_stream():
        result = await agent.call_agent_async(text)
        event = TextMessageContentEvent(
            type=EventType.TEXT_MESSAGE_CONTENT,
            message_id=message_id,
            delta=result,
        )
        yield encoder.encode(event)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
