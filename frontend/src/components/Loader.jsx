
function Loader({ message = "Processing..." }) {
  return (
    <span
      className="inline-flex items-center justify-center gap-2"
      role="status"
      aria-live="polite"
    >
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      <span>{message}</span>
    </span>
  );
}

export default Loader;
