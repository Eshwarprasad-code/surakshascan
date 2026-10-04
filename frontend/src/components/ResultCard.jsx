import { useState } from "react";

const RISK_STYLES = {
  Safe: { bg: "bg-emerald-50", border: "border-emerald-300", text: "text-emerald-700", bar: "bg-emerald-500", icon: "✅" },
  Suspicious: { bg: "bg-amber-50", border: "border-amber-300", text: "text-amber-700", bar: "bg-amber-500", icon: "⚠️" },
  "High Risk": { bg: "bg-red-50", border: "border-red-300", text: "text-red-700", bar: "bg-red-500", icon: "🚨" },
};

// Category text comes from the LLM's own wording, not a fixed enum, so we
// match loosely by keyword rather than an exact lookup table.
function getCategoryIcon(category) {
  const c = (category || "").toLowerCase();
  if (c.includes("upi") || c.includes("payment")) return "💳";
  if (c.includes("kyc") || c.includes("bank")) return "🏦";
  if (c.includes("courier") || c.includes("customs") || c.includes("parcel") || c.includes("delivery")) return "📦";
  if (c.includes("lottery") || c.includes("prize") || c.includes("lucky")) return "🎉";
  if (c.includes("job") || c.includes("work from home") || c.includes("employment")) return "💼";
  if (c.includes("arrest") || c.includes("police") || c.includes("cbi") || c.includes("legal")) return "🚔";
  if (c.includes("account") || c.includes("social") || c.includes("suspend")) return "📱";
  if (c.includes("phishing") || c.includes("scam") || c.includes("spam")) return "🚩";
  if (c === "none" || !c) return "✅";
  return "🔍";
}

const DIVIDER = "────────────────────";

export default function ResultCard({ result, t }) {
  const [copied, setCopied] = useState(false);
  if (!result) return null;
  const style = RISK_STYLES[result.risk_level] ?? RISK_STYLES.Suspicious;
  const riskLabel = t.riskLevelLabels[result.risk_level] ?? result.risk_level;

  // WhatsApp, Telegram, and most chat apps render *text* as bold and
  // _text_ as italic automatically, so this reads as a properly
  // formatted report rather than a flat data dump.
  const reportText = `🛡️ *SurakshaScan Report*
${DIVIDER}
${style.icon} *Risk Level:* ${result.risk_level} (${result.risk_score}/100)
${getCategoryIcon(result.category)} *Category:* ${result.category}
🌐 *Language:* ${result.language_detected}

📝 *Why:*
${result.explanation}

✅ *What to do:*
${result.recommended_action}
${DIVIDER}
_Checked via SurakshaScan — report scams to 1930 or cybercrime.gov.in_`;

  const handleCopy = () => {
    navigator.clipboard.writeText(reportText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({ title: "SurakshaScan report", text: reportText });
      } catch {
        // user cancelled the share sheet — not an error worth surfacing
      }
    } else {
      handleCopy();
    }
  };

  return (
    <div className={`result-card-enter w-full max-w-2xl mx-auto mt-6 rounded-xl border ${style.border} ${style.bg} p-6`}>
      <div className="flex items-center justify-between">
        <h3 className={`text-lg font-semibold ${style.text} flex items-center gap-2`}>
          <span>{style.icon}</span> {riskLabel}
        </h3>
        <span className="text-sm text-slate-500">{t.scoreLabel}: {result.risk_score}/100</span>
      </div>

      <div className="w-full h-2 bg-slate-200 rounded-full mt-2 overflow-hidden">
        <div className={`h-full ${style.bar} transition-all duration-500`} style={{ width: `${result.risk_score}%` }} />
      </div>

      <p className="mt-4 text-sm text-slate-600 flex items-center gap-1.5">
        <span>{getCategoryIcon(result.category)}</span>
        <span className="font-medium">{t.categoryLabel}</span> {result.category}
      </p>

      <p className="mt-2 text-slate-800">{result.explanation}</p>

      <div className="mt-4 p-3 rounded-lg bg-white border border-slate-200">
        <p className="text-sm font-medium text-slate-700">{t.recommendedActionLabel}</p>
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

      <div className="mt-4 flex items-center gap-4 relative">
        <button
          onClick={handleShare}
          className="cursor-pointer text-sm text-indigo-600 hover:text-indigo-800 font-medium"
        >
          {t.shareButton}
        </button>
        <button
          onClick={handleCopy}
          className="cursor-pointer text-sm text-indigo-600 hover:text-indigo-800 font-medium"
        >
          {t.copyButton}
        </button>
        {copied && (
          <span className="text-xs text-emerald-600 font-medium animate-pulse">
            {t.copiedToast}
          </span>
        )}
      </div>
    </div>
  );
}