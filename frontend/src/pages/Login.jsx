import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Login() {
  const nav = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const { data } = await api.post("/auth/login", { username, password });
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("username", data.username);
      localStorage.setItem("role", data.role);
      nav("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-page">
      <section className="login-left">
        <div className="brand-lg"><span>GIS</span></div>
        <p className="eyebrow">Geographic Information System (GIS)</p>
        <h1>Network<br />Infrastructure<br /><em>Intelligence.</em></h1>
        <p className="lead">
          A Unified Geographic Information System (GIS) for Planning, Managing and Monitoring
          Network Infrastructure.
        </p>
        <ul>
          <li>Fiber Network Mapping</li>
          <li>Infrastructure Management</li>
          <li>Real-Time Network Visibility</li>
          <li>Network Asset Intelligence</li>
          <li>Field Data &amp; Photo Capture</li>
          <li>Secure Role-Based Access</li>
        </ul>
      </section>

      <section className="login-right">
        <div className="brand-md"><span>GIS</span></div>
        <p className="eyebrow light">NETWORK INFRASTRUCTURE</p>
        <h2>GIS Portal</h2>
        <p className="muted">Secure access to Network Infrastructure.</p>

        <form className="card" onSubmit={submit}>
          <h3>Secure Access</h3>
          <small>Sign in to continue to GIS</small>
          <label>Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus required />
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          {error && <div className="error">{error}</div>}
          <button disabled={busy}>{busy ? "Signing in…" : "Sign in to GIS →"}</button>
          <div className="secure">Secure authenticated access</div>
        </form>

        <p className="legal">
          GIS · INTERNAL · CONFIDENTIAL — AUTHORISED ACCESS ONLY. Unauthorised access, use,
          disclosure or distribution is strictly prohibited.
        </p>
      </section>
    </div>
  );
}
