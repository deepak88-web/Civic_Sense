
const Footer = () => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-3 px-6 py-6 sm:flex-row">

        <div>
          <h2 className="font-semibold text-white">
            Civic<span className="text-blue-500">Sense</span>
          </h2>
          <p className="mt-1 text-xs text-slate-500">
            Multilingual Civic Complaint Classification System
          </p>
        </div>

        <p className="text-xs text-slate-500">
          Powered by LSTM & Word2Vec
        </p>

        <p className="text-xs text-slate-500">
          © {new Date().getFullYear()} CivicSense
        </p>

      </div>
    </footer>
  );
};

export default Footer;
