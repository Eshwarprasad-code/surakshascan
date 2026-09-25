const RISK_STYLES = {
  Safe: { bg: "bg-emerald-50", border: "border-emerald-300", text: "text-emerald-700", bar: "bg-emerald-500" },
  Suspicious: { bg: "bg-amber-50", border: "border-amber-300", text: "text-amber-700", bar: "bg-amber-500" },
  "High Risk": { bg: "bg-red-50", border: "border-red-300", text: "text-red-700", bar: "bg-red-500" },
};

export default function ResultCard({ result }) {
  if (!result) return null;
  const style = RISK_STYLES[result.risk_level] ?? RISK_STYLES.Suspicious;

  const handleCopy = () => {
    const report = `Risk: ${result.risk_level} (${result.risk_score}/100)
Category: ${result.category}
Language: ${result.language_detected}
Explanation: ${result.explanation}
Recommended action: ${result.recommended_action}`;
    navigator.clipboard.writeText(report);
  };

  return (
    <div className={`w-full max-w-2xl mx-auto mt-6 rounded-xl border ${style.border} ${style.bg} p-6`}>
      <div className="flex items-center justify-between">
        <h3 className={`text-lg font-semibold ${style.text}`}>{result.risk_level}</h3>
        <span className="text-sm text-slate-500">Score: {result.risk_score}/100</span>
      </div>

      <div className="w-full h-2 bg-slate-200 rounded-full mt-2 overflow-hidden">
        <div className={`h-full ${style.bar}`} style={{ width: `${result.risk_score}%` }} />
      </div>

      <p className="mt-4 text-sm text-slate-600">
        <span className="font-medium">Category:</span> {result.category}
      </p>

      <p className="mt-2 text-slate-800">{result.explanation}</p>

      <div className="mt-4 p-3 rounded-lg bg-white border border-slate-200">
        <p className="text-sm font-medium text-slate-700">Recommended action</p>
        <p className="text-slate-800 mt-1">{result.recommended_action}</p>
      </div>

      {result.heuristic_flags?.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {result.heuristic_flags.map((flag, i) => (
            <span key={i} className="text-xs px-2 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
              {flag}
            </span>
          ))}
        </div>
      )}

      <button
        onClick={handleCopy}
        className="mt-4 text-sm text-indigo-600 hover:text-indigo-800 font-medium"
      >
        Copy report
      </button>
    </div>
  );
}
