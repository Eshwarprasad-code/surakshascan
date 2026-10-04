import { useState, useEffect, useRef } from "react";
import MessageInput from "./components/MessageInput";
import ResultCard from "./components/ResultCard";

// Container component: owns state + the API call. Presentational
// components (MessageInput, ResultCard) just render props.
const API_BASE = import.meta.env.VITE_API_BASE || "/api";

const EXAMPLES = [
  {
    label: "UPI fraud (EN)",
    text: "Someone tried logging into your BHIM UPI account from a new device, share the OTP received to cancel the transaction immediately.",
  },
  {
    label: "Fake KYC (HI)",
    text: "आपका बैंक खाता सत्यापन लंबित है, कृपया तुरंत अपडेट करें",
  },
  {
    label: "Data pack scam (TE)",
    text: "డేటా ప్యాక్ గడువు ముగిసింది! డేటా ప్యాక్‌ని కొనుగోలు చేయడానికి - http://tiny.jio.com/dbuydatapack",
  },
  {
    label: "Safe bank alert (EN)",
    text: "HDFC Bank: Rs 2,499 debited from account XX6792. Available balance Rs 36925.00",
  },
];

export default function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const timerRef = useRef(null);

  useEffect(() => {
    if (loading) {
      setElapsed(0);
      timerRef.current = setInterval(() => setElapsed((s) => s + 1), 1000);
    } else {
      clearInterval(timerRef.current);
    }
    return () => clearInterval(timerRef.current);
  }, [loading]);

  const handleAnalyze = async (overrideText) => {
    const textToSend = overrideText ?? message;
    if (!textToSend.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: textToSend }),
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

  const handleExampleClick = (text) => {
    setMessage(text);
    handleAnalyze(text);
  };

  return (
    <div
      className="min-h-screen bg-slate-50 px-4"
      style={{
        paddingTop: "max(3rem, env(safe-area-inset-top, 0px))",
        paddingBottom: "max(3rem, env(safe-area-inset-bottom, 0px))",
      }}
    >
      <div className="max-w-2xl mx-auto text-center mb-6">
        <h1 className="text-3xl font-bold text-slate-900 flex items-center justify-center gap-2">
          <span>🛡️</span> SurakshaScan
        </h1>
        <p className="text-slate-600 mt-2">
          Paste a suspicious message and get an instant, plain-language safety check —
          English, Hindi, or Telugu.
        </p>
      </div>

      <div className="max-w-2xl mx-auto mb-6">
        <p className="text-xs text-slate-500 mb-2 text-center">Try an example:</p>
        <div className="flex flex-wrap justify-center gap-2">
          {EXAMPLES.map((ex) => (
            <button
              key={ex.label}
              onClick={() => handleExampleClick(ex.text)}
              disabled={loading}
              className="cursor-pointer text-xs px-3 py-1.5 rounded-full border border-slate-300 bg-white text-slate-600 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed transition"
            >
              {ex.label}
            </button>
          ))}
        </div>
      </div>

      <MessageInput
        value={message}
        onChange={setMessage}
        onSubmit={() => handleAnalyze()}
        loading={loading}
      />

      {loading && (
        <p className="max-w-2xl mx-auto mt-3 text-center text-xs text-slate-400">
          {elapsed < 8
            ? "Analyzing..."
            : "Still working — the server may be waking up from idle, this can take up to a minute on the first request."}
        </p>
      )}

      {error && (
        <div className="w-full max-w-2xl mx-auto mt-4 rounded-xl border border-red-300 bg-red-50 p-4 text-center">
          <p className="text-red-700 text-sm">{error}</p>
          <button
            onClick={() => handleAnalyze()}
            className="cursor-pointer mt-2 text-sm text-red-700 underline font-medium hover:text-red-900"
          >
            Try again
          </button>
        </div>
      )}

      <ResultCard result={result} />

      <p className="max-w-2xl mx-auto mt-10 text-center text-xs text-slate-400">
        Your message is analyzed instantly and not stored. If in doubt, report suspicious
        messages to the National Cyber Crime Helpline: 1930 or cybercrime.gov.in
      </p>
    </div>
  );
}