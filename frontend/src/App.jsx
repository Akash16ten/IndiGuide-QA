import { useState } from "react";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState([]);


  async function askQuestion() {
    setLoading(true);
    setAnswer("");

    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
setAnswer(data.answer);
setSources(data.sources || []);
    setLoading(false);
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        color: "white",
        fontFamily: "system-ui"
      }}
    >
      <div style={{ width: "420px", background: "#111", padding: "24px", borderRadius: "12px" }}>
        <h2>IndiGuide-QA</h2>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about an Indian government scheme"
          style={{ width: "100%", height: "80px", marginBottom: "12px" }}

          onKeyDown={(e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    askQuestion();
  }
}}

        />

        <button
  onClick={askQuestion}
  disabled={loading}
  className="ask-btn"
>
  {loading ? "Thinking..." : "Ask"}
</button>

{answer && (
  <div className="answer-box">
    <h3>Answer</h3>
    <p style={{ whiteSpace: "pre-wrap" }}>{answer}</p>

    {sources.length > 0 && (
      <>
        <h4>Sources:</h4>
        <ul>
          {sources.map((src, i) => (
            <li key={i}>{src}</li>
          ))}
        </ul>
      </>
    )}
  </div>
)}


      </div>
    </div>
  );
}
