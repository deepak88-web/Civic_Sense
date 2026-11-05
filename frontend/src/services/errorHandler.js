
export function getApiErrorMessage(error) {
  if (error.response) {
    const detail = error.response.data?.detail;

    if (Array.isArray(detail)) {
      return detail
        .map((item) => item.msg || "Invalid input")
        .join(", ");
    }

    if (typeof detail === "string") {
      return detail;
    }

    return `Request failed with status ${error.response.status}.`;
  }

  if (error.request) {
    return "Unable to connect to the CivicSense server. Please check whether the backend is running.";
  }

  return error.message || "Something went wrong. Please try again.";
}
