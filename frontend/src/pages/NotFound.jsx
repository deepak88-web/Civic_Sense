
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="flex min-h-[65vh] flex-col items-center justify-center px-4 text-center">
      <h1 className="text-8xl font-extrabold tracking-tight text-blue-500">
        404
      </h1>

      <h2 className="mt-4 text-2xl font-bold text-white">
        Page Not Found
      </h2>

      <p className="mt-3 max-w-md text-slate-400">
        The page you're looking for doesn't exist or may have been moved.
      </p>

      <Link
        to="/"
        className="mt-8 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-500"
      >
        Back to Home
      </Link>
    </div>
  );
}

export default NotFound;
