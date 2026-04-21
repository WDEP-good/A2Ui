import { useState } from "react";
import type { FormEvent } from "react";
import { runAgentWithHttpConfig } from "../utils";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!input.trim() || loading) return;

    setLoading(true);
    setOutput("");
    setError("");
    try {
      const result = await runAgentWithHttpConfig(input);
      setOutput(result);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <h1>AGUI Demo</h1>
      <form onSubmit={onSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="输入问题..."
        />
        <button type="submit" disabled={loading}>
          {loading ? "生成中..." : "发送"}
        </button>
      </form>
      {error ? <p>{error}</p> : null}
      <pre>{output}</pre>
    </main>
  );
}

export default App;
