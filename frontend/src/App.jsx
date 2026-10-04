import { useState, useEffect, useRef } from "react";
import MessageInput from "./components/MessageInput";
import ResultCard from "./components/ResultCard";
import { LANGUAGES, translations } from "./i18n";

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
  const [uiLang, setUiLang] = useState("en");
  const t = translations[uiLang];

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
      if (!res.ok) {
        let detail = null;
        try {
          detail = (await res.json()).detail;
        } catch {
          // response wasn't JSON — fall through to the generic message
        }
        setError(res.status === 429 ? detail || t.errorRateLimit : t.errorGeneric);
        return;
      }
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(t.errorGeneric);
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
      <div className="max-w-2xl mx-auto flex justify-end mb-2">
        <div className="inline-flex rounded-full border border-slate-300 bg-white p-0.5">
          {LANGUAGES.map((l) => (
            <button
              key={l.code}
              onClick={() => setUiLang(l.code)}
              className={`cursor-pointer text-xs px-3 py-1 rounded-full transition ${
                uiLang === l.code
                  ? "bg-indigo-600 text-white"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              {l.label}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-2xl mx-auto text-center mb-6">
        <h1 className="text-3xl font-bold text-slate-900 flex items-center justify-center gap-2">
          <span>🛡️</span> SurakshaScan
        </h1>
        <p className="text-slate-600 mt-2">{t.subtitle}</p>
      </div>

      <div className="max-w-2xl mx-auto mb-6">
        <p className="text-xs text-slate-500 mb-2 text-center">{t.tryExample}</p>
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
        t={t}
      />

      {loading && (
        <p className="max-w-2xl mx-auto mt-3 text-center text-xs text-slate-400">
          {elapsed < 8 ? t.analyzingButton : t.wakingHint}
        </p>
      )}

      {error && (
        <div className="w-full max-w-2xl mx-auto mt-4 rounded-xl border border-red-300 bg-red-50 p-4 text-center">
          <p className="text-red-700 text-sm">{error}</p>
          <button
            onClick={() => handleAnalyze()}
            className="cursor-pointer mt-2 text-sm text-red-700 underline font-medium hover:text-red-900"
          >
            {t.tryAgain}
          </button>
        </div>
      )}

      <ResultCard result={result} t={t} />

      <p className="max-w-2xl mx-auto mt-10 text-center text-xs text-slate-400">
        {t.footerDisclaimer}
      </p>
    </div>
  );
}