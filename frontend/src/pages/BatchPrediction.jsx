
import { useRef, useState } from "react";
import API from "../services/api";
import Loader from "../components/Loader";
import { getApiErrorMessage } from "../services/errorHandler";

const BatchPrediction = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    setError("");
    setResult(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setFile(null);
      setError("Please select a CSV file.");
      event.target.value = "";
      return;
    }

    setFile(selectedFile);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await API.post("/predict/batch", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(getApiErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!result?.output_filename) return;

    try {
      const response = await API.get(
        `/predict/batch/download/${encodeURIComponent(
          result.output_filename
        )}`,
        { responseType: "blob" }
      );

      const downloadUrl = window.URL.createObjectURL(response.data);
      const link = document.createElement("a");

      link.href = downloadUrl;
      link.download = result.output_filename;

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(downloadUrl);
    } catch {
      setError("Unable to download the prediction file. Please try again.");
    }
  };

  const confidenceCards = [
    {
      label: "High Confidence",
      count: result?.high_confidence_count ?? 0,
      color: "text-emerald-400",
      background: "bg-emerald-500/10",
      border: "border-emerald-500/20",
    },
    {
      label: "Medium Confidence",
      count: result?.medium_confidence_count ?? 0,
      color: "text-amber-400",
      background: "bg-amber-500/10",
      border: "border-amber-500/20",
    },
    {
      label: "Low Confidence",
      count: result?.low_confidence_count ?? 0,
      color: "text-red-400",
      background: "bg-red-500/10",
      border: "border-red-500/20",
    },
  ];

  return (
    <div className="mx-auto max-w-5xl">

      {/* Page Heading */}
      <div className="mb-10 text-center">
        <p className="text-sm font-semibold uppercase tracking-widest text-teal-400">
          Bulk Classification
        </p>

        <h1 className="mt-3 text-3xl font-bold text-white sm:text-4xl">
          Batch Complaint Prediction
        </h1>

        <p className="mx-auto mt-4 max-w-2xl leading-7 text-slate-400">
          Upload a CSV file containing multiple civic complaints.
          CivicSense will classify them and generate a downloadable
          results file.
        </p>
      </div>

      {/* Upload Section */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 sm:p-8">

        <form onSubmit={handleSubmit}>
          <label className="mb-4 block font-semibold text-white">
            Upload Complaint Dataset
          </label>

          <div
            onClick={() => fileInputRef.current?.click()}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                fileInputRef.current?.click();
              }
            }}
            role="button"
            tabIndex={0}
            className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-700 bg-slate-950 px-5 py-12 text-center transition hover:border-teal-500 hover:bg-teal-500/5"
          >
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-500/10 text-3xl">
              📁
            </div>

            <p className="font-semibold text-white">
              {file ? file.name : "Click to browse your CSV file"}
            </p>

            <p className="mt-2 text-sm text-slate-500">
              CSV files only
            </p>

            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,text/csv"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>

          {file && (
            <div className="mt-4 flex items-center justify-between rounded-lg border border-slate-700 bg-slate-950 p-4">
              <div>
                <p className="text-sm font-medium text-white">
                  {file.name}
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>

              <button
                type="button"
                onClick={() => {
                  setFile(null);
                  setResult(null);
                  setError("");
                  if (fileInputRef.current) {
                    fileInputRef.current.value = "";
                  }
                }}
                className="text-sm text-red-400 hover:text-red-300"
              >
                Remove
              </button>
            </div>
          )}

          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm font-semibold text-slate-300">
              CSV file requirements
            </p>

            <ul className="mt-3 list-inside list-disc space-y-2 text-sm text-slate-500">
              <li>File format must be CSV.</li>
              <li>Must contain a column named complaint_text.</li>
              <li>Complaint entries must not be empty.</li>
              <li>Other columns will be preserved in the output.</li>
            </ul>
          </div>

          {error && (
            <div className="mt-5 rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !file}
            className="mt-7 flex w-full items-center justify-center gap-2 rounded-xl bg-teal-600 px-6 py-3.5 font-semibold text-white transition hover:bg-teal-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? (
              <Loader message="Processing CSV..." />
            ) : (
              "Upload and Predict"
            )}
          </button>
        </form>
      </div>

      {/* Prediction Summary */}
      {result && (
        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6 sm:p-8">

          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-teal-400">
                Processing Complete
              </p>

              <h2 className="mt-2 text-2xl font-bold text-white">
                Prediction Summary
              </h2>
            </div>

            <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm font-semibold text-emerald-400">
              Successful
            </span>
          </div>

          <div className="mt-7 rounded-xl border border-slate-800 bg-slate-950 p-5">
            <p className="text-sm text-slate-400">
              Total Complaints Processed
            </p>

            <h3 className="mt-2 text-4xl font-bold text-white">
              {result.total_complaints}
            </h3>
          </div>

          <div className="mt-5 grid gap-4 sm:grid-cols-3">
            {confidenceCards.map((card) => (
              <div
                key={card.label}
                className={`rounded-xl border ${card.border} ${card.background} p-5`}
              >
                <p className="text-sm text-slate-400">
                  {card.label}
                </p>

                <h3 className={`mt-3 text-3xl font-bold ${card.color}`}>
                  {card.count}
                </h3>
              </div>
            ))}
          </div>

          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm text-slate-400">
              Output File
            </p>

            <p className="mt-2 break-all font-medium text-white">
              {result.output_filename}
            </p>
          </div>

          <button
            onClick={handleDownload}
            className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3.5 font-semibold text-white transition hover:bg-blue-500"
          >
            Download Prediction CSV ↓
          </button>

          <p className="mt-4 text-center text-xs text-slate-500">
            {result.message}
          </p>

        </div>
      )}

    </div>
  );
};

export default BatchPrediction;
