import { useMemo, useState } from "react";
import { createPrediction, signPayload } from "../services/api";

const initialPayload = {
  age: 32,
  monthly_income: 9000,
  credit_score: 710,
  loan_amount: 100000,
  loan_term_months: 180,
};

export function App() {
  const [payload, setPayload] = useState(initialPayload);
  const [result, setResult] = useState(null);

  const prettyPayload = useMemo(() => JSON.stringify(payload, null, 2), [payload]);

  async function submit() {
    const signature = await signPayload(payload);
    const response = await createPrediction(payload, signature);
    setResult(response);
  }

  return (
    <main className="layout">
      <h1>MLOps Production Pipeline</h1>
      <p>Real-time credit risk scoring service with observability hooks.</p>
      <button onClick={submit}>Run Inference</button>
      <section>
        <h2>Input Event</h2>
        <pre>{prettyPayload}</pre>
      </section>
      <section>
        <h2>Prediction</h2>
        <pre>{result ? JSON.stringify(result, null, 2) : "No result yet"}</pre>
      </section>
    </main>
  );
}
