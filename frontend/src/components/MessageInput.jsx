export default function MessageInput({ value, onChange, onSubmit, loading }) {
  return (
    <div className="w-full max-w-2xl mx-auto">
      <textarea
        className="w-full h-40 p-4 rounded-xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none resize-none text-base"
        placeholder="Paste the suspicious SMS, WhatsApp message, or email here... (English, Hindi, or Telugu)"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        maxLength={4000}
      />
      <div className="flex justify-between items-center mt-3">
        <span className="text-sm text-slate-500">{value.length}/4000</span>
        <button
          onClick={onSubmit}
          disabled={loading || value.trim().length === 0}
          className="px-6 py-2.5 rounded-lg bg-indigo-600 text-white font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:bg-indigo-700 transition"
        >
          {loading ? "Analyzing..." : "Analyze Message"}
        </button>
      </div>
    </div>
  );
}
