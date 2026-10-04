export default function MessageInput({ value, onChange, onSubmit, loading, t }) {
  return (
    <div className="w-full max-w-2xl mx-auto">
      <textarea
        className="w-full h-40 p-4 rounded-xl border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none resize-none text-base"
        placeholder={t.placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        maxLength={4000}
      />
      <div className="flex flex-col-reverse sm:flex-row sm:justify-between sm:items-center gap-3 mt-3">
        <span className="text-sm text-slate-500 text-center sm:text-left">{value.length}/4000</span>
        <button
          onClick={onSubmit}
          disabled={loading || value.trim().length === 0}
          className="cursor-pointer w-full sm:w-auto px-6 py-2.5 rounded-lg bg-indigo-600 text-white font-medium disabled:opacity-70 disabled:cursor-not-allowed hover:bg-indigo-700 active:bg-indigo-800 transition flex items-center justify-center gap-2"
        >
          {loading && (
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          )}
          {loading ? t.analyzingButton : t.analyzeButton}
        </button>
      </div>
    </div>
  );
}