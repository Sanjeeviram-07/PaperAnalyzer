const API_BASE = process.env.REACT_APP_API_URL;

export async function getData() {
  const res = await fetch(`${API_BASE}/`);
  return res.json();
}
