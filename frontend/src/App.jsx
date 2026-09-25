import { useState } from "react";
import MessageInput from "./components/MessageInput";
import ResultCard from "./components/ResultCard";

// Container component: owns state + the API call. Presentational
// components (MessageInput, ResultCard) just render props.
const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export default function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Couldn't analyze that message right now. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4">
      <div className="max-w-2xl mx-auto text-center mb-8">
        <h1 className="text-3xl font-bold text-slate-900">SurakshaScan</h1>
        <p className="text-slate-600 mt-2">
          Paste a suspicious message and get an instant, plain-language safety check —
          English, Hindi, or Telugu.
        </p>
      </div>

      <MessageInput
        value={message}
        onChange={setMessage}
        onSubmit={handleAnalyze}
        loading={loading}
      />

      {error && (
        <p className="max-w-2xl mx-auto mt-4 text-center text-red-600 text-sm">{error}</p>
      )}

      <ResultCard result={result} />

      <p className="max-w-2xl mx-auto mt-10 text-center text-xs text-slate-400">
        Your message is analyzed instantly and not stored. If in doubt, report suspicious
        messages to the National Cyber Crime Helpline: 1930 or cybercrime.gov.in
      </p>
    </div>
  );
}
