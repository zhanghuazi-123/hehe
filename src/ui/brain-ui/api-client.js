export const API = /^https?:$/.test(window.location?.protocol || "")
  ? window.location.origin
  : "http://localhost:3722";

export function apiUrl(path) {
  return `${API}${path}`;
}

