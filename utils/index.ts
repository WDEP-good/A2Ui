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
  url: "/agent",
};

const agent = new HttpAgent(config);
// agent.subscribe(new AgentSubscriber({
//     onMessage: (message) => {
//         console.log(message)
//     }
// }))

// const parameters: RunAgentParameters = {
//   runId: "",
//   tools: [],
//   context: [{ value: "Hello, world!", description: "Hello, world!" }],
// };
// agent
//   .runAgent(parameters)
//   .then((result) => {
//     console.log(result);
//   })
//   .catch((error) => {
//     console.error(error);
//   });

export async function runAgentWithHttpConfig(
  requestText: string,
): Promise<string> {
  const parameters: RunAgentParameters = {
    runId: crypto.randomUUID(),
    tools: [],
    context: [{ value: requestText, description: "user_input" }],
  };

  const result = await agent.runAgent(parameters);
  return typeof result === "string" ? result : JSON.stringify(result);
}
