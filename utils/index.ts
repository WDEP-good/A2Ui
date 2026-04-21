import {
  HttpAgent,
  type HttpAgentConfig,
  type RunAgentParameters,
} from "@ag-ui/client";

const config: HttpAgentConfig = {
  agentId: "agent_123",
  description: "A helpful assistant for user questions.",
  threadId: "thread_123",
  initialMessages: [],
  initialState: {},
  url: "http://localhost:3000/agent",
};

const agent = new HttpAgent(config);
// agent.subscribe(new AgentSubscriber({
//     onMessage: (message) => {
//         console.log(message)
//     }
// }))

const parameters: RunAgentParameters = {
  runId: "",
  tools: [],
  context: [{ value: "Hello, world!", description: "Hello, world!" }],
};
agent
  .runAgent(parameters)
  .then((result) => {
    console.log(result);
  })
  .catch((error) => {
    console.error(error);
  });
