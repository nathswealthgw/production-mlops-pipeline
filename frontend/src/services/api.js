import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  timeout: 5000,
});

const encoder = new TextEncoder();

export async function signPayload(payload) {
  const raw = JSON.stringify(payload);
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode("change-me"),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );

  const signature = await crypto.subtle.sign("HMAC", key, encoder.encode(raw));
  return Array.from(new Uint8Array(signature))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

export async function createPrediction(payload, signature) {
  const response = await api.post("/predictions", payload, {
    headers: { "x-signature": signature },
  });

  return response.data;
}
