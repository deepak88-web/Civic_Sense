
import { Link } from "react-router-dom";

const Home = () => {
  const features = [
    {
      icon: "🌐",
      title: "Multilingual Support",
      description:
        "Classify civic complaints written in multiple languages, making the system accessible to diverse communities.",
    },
    {
      icon: "🧠",
      title: "AI-Powered Classification",
      description:
        "Uses an LSTM neural network with Word2Vec embeddings to understand complaint context and predict categories.",
    },
    {
      icon: "📊",
      title: "Confidence Analysis",
      description:
        "Every prediction includes a confidence score and a confidence level to help assess model reliability.",
    },
    {
      icon: "⚡",
      title: "Batch Processing",
      description:
        "Upload CSV files and classify multiple civic complaints in a single operation.",
    },
  ];

  return (
    <div className="space-y-24">

      {/* Hero Section */}
      <section className="grid items-center gap-12 py-12 lg:grid-cols-2 lg:py-20">

        <div>
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-2 text-sm text-blue-400">
            <span className="h-2 w-2 rounded-full bg-blue-400"></span>
            Intelligent Civic Complaint Classification
          </div>

          <h1 className="text-4xl font-bold leading-tight tracking-tight text-white sm:text-5xl lg:text-6xl">
            Making Civic
            <span className="block text-blue-500">
              Complaints
            </span>
            Easier to Understand.
          </h1>

          <p className="mt-6 max-w-xl text-base leading-8 text-slate-400 sm:text-lg">
            CivicSense uses artificial intelligence to classify
            multilingual civic complaints into meaningful categories.
            Helping transform everyday public concerns into structured
            information.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/predict"
              className="rounded-xl bg-blue-600 px-6 py-3.5 font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500"
            >
              Try Single Prediction →
            </Link>

            <Link
              to="/batch-predict"
              className="rounded-xl border border-slate-700 px-6 py-3.5 font-semibold text-slate-300 transition hover:border-blue-500 hover:text-white"
            >
              Explore Batch Prediction
            </Link>
          </div>

          <div className="mt-10 flex flex-wrap gap-8 border-t border-slate-800 pt-8">
            <div>
              <h3 className="text-2xl font-bold text-white">12</h3>
              <p className="mt-1 text-sm text-slate-500">
                Complaint Categories
              </p>
            </div>

            <div>
              <h3 className="text-2xl font-bold text-white">LSTM</h3>
              <p className="mt-1 text-sm text-slate-500">
                Deep Learning Model
              </p>
            </div>

            <div>
              <h3 className="text-2xl font-bold text-white">Word2Vec</h3>
              <p className="mt-1 text-sm text-slate-500">
                Word Embeddings
              </p>
            </div>
          </div>
        </div>

        {/* Right Side Illustration */}
        <div className="relative">
          <div className="absolute -inset-6 rounded-full bg-blue-600/10 blur-3xl"></div>

          <div className="relative rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl sm:p-8">

            <div className="flex items-center justify-between border-b border-slate-800 pb-5">
              <div>
                <p className="text-sm font-medium text-slate-400">
                  Prediction Overview
                </p>
                <h3 className="mt-1 text-xl font-bold text-white">
                  Complaint Analysis
                </h3>
              </div>

              <div className="rounded-xl bg-blue-500/10 p-3 text-2xl">
                🏙️
              </div>
            </div>

            <div className="mt-6 rounded-xl border border-slate-700 bg-slate-950 p-5">
              <p className="text-xs font-medium uppercase tracking-wider text-slate-500">
                Sample Complaint
              </p>

              <p className="mt-3 leading-7 text-slate-300">
                "There is a large pothole on the main road near our
                residential area."
              </p>
            </div>

            <div className="mt-5 flex items-center justify-between rounded-xl bg-slate-800/70 p-4">
              <div>
                <p className="text-xs text-slate-400">
                  Predicted Category
                </p>
                <h4 className="mt-1 font-semibold text-white">
                  Road Infrastructure
                </h4>
              </div>

              <div className="rounded-lg bg-emerald-500/10 px-3 py-2 text-sm font-semibold text-emerald-400">
                High
              </div>
            </div>

            <div className="mt-5">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Confidence Score
                </span>
                <span className="font-semibold text-blue-400">
                  85.2%
                </span>
              </div>

              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-800">
                <div className="h-full w-[85.2%] rounded-full bg-blue-500"></div>
              </div>
            </div>

            <p className="mt-5 text-center text-xs text-slate-500">
              Illustrative prediction example
            </p>
          </div>
        </div>

      </section>

      {/* Prediction Options */}
      <section>
        <div className="mb-10 text-center">
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
            Get Started
          </p>

          <h2 className="mt-3 text-3xl font-bold text-white sm:text-4xl">
            Choose Your Prediction Mode
          </h2>

          <p className="mx-auto mt-4 max-w-2xl text-slate-400">
            Analyze a single complaint or process an entire dataset
            using our classification system.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">

          {/* Single Prediction Card */}
          <div className="group rounded-2xl border border-slate-800 bg-slate-900 p-8 transition hover:-translate-y-1 hover:border-blue-500/50">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-500/10 text-3xl">
              💬
            </div>

            <h3 className="mt-6 text-2xl font-bold text-white">
              Single Complaint
            </h3>

            <p className="mt-3 leading-7 text-slate-400">
              Enter an individual civic complaint and receive its
              predicted category, confidence score and confidence level.
            </p>

            <Link
              to="/predict"
              className="mt-8 inline-flex items-center gap-2 font-semibold text-blue-400 transition group-hover:text-blue-300"
            >
              Classify a Complaint →
            </Link>
          </div>

          {/* Batch Prediction Card */}
          <div className="group rounded-2xl border border-slate-800 bg-slate-900 p-8 transition hover:-translate-y-1 hover:border-teal-500/50">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-500/10 text-3xl">
              📁
            </div>

            <h3 className="mt-6 text-2xl font-bold text-white">
              Batch Complaints
            </h3>

            <p className="mt-3 leading-7 text-slate-400">
              Upload a CSV containing multiple complaints, generate
              predictions and download the classified results.
            </p>

            <Link
              to="/batch-predict"
              className="mt-8 inline-flex items-center gap-2 font-semibold text-teal-400 transition group-hover:text-teal-300"
            >
              Process CSV File →
            </Link>
          </div>

        </div>
      </section>

      {/* Features Section */}
      <section className="pb-12">
        <div className="mb-10 text-center">
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-400">
            Why CivicSense?
          </p>

          <h2 className="mt-3 text-3xl font-bold text-white sm:text-4xl">
            Built for Smarter Classification
          </h2>
        </div>

        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 transition hover:border-slate-600"
            >
              <div className="text-3xl">{feature.icon}</div>

              <h3 className="mt-5 font-semibold text-white">
                {feature.title}
              </h3>

              <p className="mt-3 text-sm leading-7 text-slate-400">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
};

export default Home;
