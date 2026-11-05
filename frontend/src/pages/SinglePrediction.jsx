
import { useState } from "react";
import API from "../services/api";
import Loader from "../components/Loader";
import { getApiErrorMessage } from "../services/errorHandler";

const SinglePrediction = () => {
  const [complaint, setComplaint] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!complaint.trim()) {
      setError("Please enter a complaint before submitting.");
      return;
    }

    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const response = await API.post("/predict", {
        complaint_text: complaint.trim(),
      });

      setPrediction(response.data);
    } catch (err) {
        setError(getApiErrorMessage(err));
      } finally {
      setLoading(false);
    }
  };

  const confidenceColor = {
    High: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    Medium: "text-amber-400 bg-amber-500/10 border-amber-500/20",
    Low: "text-red-400 bg-red-500/10 border-red-500/20",
  };

  return (
    <div className="mx-auto max-w-4xl">

      {/* Page Heading */}
      <div className="mb-10 text-center">
        <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
          Individual Classification
        </p>

        <h1 className="mt-3 text-3xl font-bold text-white sm:text-4xl">
          Single Complaint Prediction
        </h1>

        <p className="mx-auto mt-4 max-w-2xl leading-7 text-slate-400">
          Enter a civic complaint in your preferred language.
          CivicSense will analyze the text and predict its category.
        </p>
      </div>

      {/* Complaint Form */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 sm:p-8">

        <form onSubmit={handleSubmit}>
          <label className="mb-3 block font-semibold text-white">
            Enter Your Complaint
          </label>

          <textarea
            value={complaint}
            onChange={(e) => setComplaint(e.target.value)}
            placeholder="Example: There is a large pothole on the main road..."
            rows={6}
            maxLength={5000}
            disabled={loading}
            className="w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-white outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-60"
          />

          <div className="mt-2 flex justify-between text-xs text-slate-500">
            <span>Supports multilingual complaints</span>
            <span>{complaint.length}/5000</span>
          </div>

          {error && (
            <div className="mt-5 rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-7 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3.5 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? (
              <Loader message="Analyzing..." />
            ) : (
              "Predict Complaint Category →"
            )}
          </button>
        </form>
      </div>

      {/* Prediction Result */}
      {prediction && (
        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6 sm:p-8">

          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white">
              Prediction Result
            </h2>

            <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-400">
              Completed
            </span>
          </div>

          <div className="mt-6 rounded-xl bg-slate-950 p-5">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Submitted Complaint
            </p>

            <p className="mt-3 leading-7 text-slate-300">
              {prediction.complaint_text}
            </p>
          </div>

          <div className="mt-5 grid gap-4 sm:grid-cols-2">

            <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
              <p className="text-sm text-slate-400">
                Predicted Category
              </p>

              <h3 className="mt-3 text-xl font-bold text-blue-400">
                {prediction.predicted_category}
              </h3>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
              <p className="text-sm text-slate-400">
                Confidence Level
              </p>

              <span
                className={`mt-3 inline-block rounded-lg border px-4 py-2 text-sm font-semibold ${
                  confidenceColor[prediction.prediction_status]
                }`}
              >
                {prediction.prediction_status}
              </span>
            </div>

          </div>

          <div className="mt-5 rounded-xl border border-slate-800 bg-slate-950 p-5">

            <div className="flex justify-between">
              <p className="text-sm text-slate-400">
                Confidence Score
              </p>

              <p className="font-bold text-white">
                {(prediction.confidence_score * 100).toFixed(2)}%
              </p>
            </div>

            <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-blue-500 transition-all duration-700"
                style={{
                  width: `${prediction.confidence_score * 100}%`,
                }}
              />
            </div>

          </div>

          <button
            onClick={() => {
              setComplaint("");
              setPrediction(null);
              setError("");
            }}
            className="mt-6 rounded-lg border border-slate-700 px-5 py-2.5 text-sm font-medium text-slate-300 transition hover:border-blue-500 hover:text-white"
          >
            Analyze Another Complaint
          </button>

        </div>
      )}

    </div>
  );
};

export default SinglePrediction;
