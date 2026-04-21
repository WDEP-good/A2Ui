from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv
import asyncio
from google.genai import types
import os

load_dotenv()

model = LiteLlm(
    model="openai/deepseek-chat",  # 使用 openai/ 前缀指定为 OpenAI 兼容接口
    api_base="https://api.deepseek.com/v1",  # DeepSeek API 端点
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

root_agent = Agent(
    model=model,
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
session_service = InMemorySessionService()
session = asyncio.run(session_service.create_session(
    app_name="test", user_id="test", session_id="test"
))
runner = Runner(agent=root_agent, app_name="test",
                session_service=session_service)

# Agent Interaction (Async)
async def call_agent_async(query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = "No final text response captured."
    try:
        # Use run_async
        async for event in runner.run_async(
            user_id="test", session_id="test", new_message=content
        ):
            # --- Check for specific parts FIRST ---
            has_specific_part = False
            if event.content and event.content.parts:
                for part in event.content.parts:  # Iterate through all parts
                    if part.executable_code:
                        has_specific_part = True
                    elif part.code_execution_result:
                        # Access outcome and output correctly
                        print(
                            f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}"
                        )
                        has_specific_part = True
                    # Also print any text parts found in any event for debugging
                    elif part.text and not part.text.isspace():
                        print(f"  Text: '{part.text.strip()}'")
                        # Do not set has_specific_part=True here, as we want the final response logic below

            # --- Check for final response AFTER specific parts ---
            # Only consider it final if it doesn't have the specific code parts we just handled
            if not has_specific_part and event.is_final_response():
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    final_response_text = event.content.parts[0].text.strip()
                else:
                    final_response_text = "No final text response captured."
    except Exception as e:
        final_response_text = f"ERROR during agent run: {e}"
    return final_response_text

# from ag_ui.core import RunAgentInput,TextMessageContentEvent, EventType
# from ag_ui.encoder import EventEncoder

# # Create an event
# event = TextMessageContentEvent(
#     type=EventType.TEXT_MESSAGE_CONTENT,
#     message_id="msg_123",
#     delta="Hello, world!"
# )

# # Initialize the encoder
# encoder = EventEncoder()

# # Encode the event
# encoded_event = encoder.encode(event)
# print(encoded_event)
# # Output: data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg_123","delta":"Hello, world!"}\n\n