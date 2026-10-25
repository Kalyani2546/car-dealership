const API_ROOT = "/api";

function readCookie(name) {
  const prefix = `${name}=`;
  return document.cookie
    .split(";")
    .map((value) => value.trim())
    .find((value) => value.startsWith(prefix))
    ?.slice(prefix.length);
}

export async function api(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const method = options.method || "GET";
  if (options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  if (!["GET", "HEAD", "OPTIONS", "TRACE"].includes(method.toUpperCase())) {
    await fetch(`${API_ROOT}/csrf/`, { credentials: "include" });
    const token = readCookie("csrftoken");
    if (token) headers.set("X-CSRFToken", decodeURIComponent(token));
  }
  const response = await fetch(`${API_ROOT}${path}`, {
    ...options,
    method,
    headers,
    credentials: "include",
  });
  let payload;
  try {
    payload = await response.json();
  } catch {
    if (!response.ok) throw new Error(`Request failed with status ${response.status}.`);
    throw new Error("The server returned an invalid response.");
  }
  if (!response.ok) {
    const message = typeof payload.error === "string"
      ? payload.error
      : Array.isArray(payload.error)
        ? payload.error.join(" ")
        : "Request failed.";
    throw new Error(message);
  }
  return payload;
}
