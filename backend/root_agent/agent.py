from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='<FILL_IN_MODEL>',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)


from ag_ui.core import RunAgentInput,TextMessageContentEvent, EventType
from ag_ui.encoder import EventEncoder

# Create an event
event = TextMessageContentEvent(
    type=EventType.TEXT_MESSAGE_CONTENT,
    message_id="msg_123",
    delta="Hello, world!"
)

# Initialize the encoder
encoder = EventEncoder()

# Encode the event
encoded_event = encoder.encode(event)
print(encoded_event)
# Output: data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg_123","delta":"Hello, world!"}\n\n