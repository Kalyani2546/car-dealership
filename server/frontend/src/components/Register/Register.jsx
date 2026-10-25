import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../../../../frontend/client/src/api.js";

export default function Register({ onRegistered }) {
  const [form, setForm] = useState({ username: "", first_name: "", last_name: "", email: "", password: "" });
  const [error, setError] = useState("");

  function update(event) {
    setForm((previous) => ({ ...previous, [event.target.name]: event.target.value }));
  }

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      await api("/register/", { method: "POST", body: JSON.stringify(form) });
      await onRegistered();
    } catch (problem) {
      setError(problem.message);
    }
  }

  return (
    <main className="form-page">
      <form className="form-card" onSubmit={submit}>
        <p className="eyebrow">Join the community</p>
        <h1>Create your account</h1>
        <p className="muted">Save time and share your dealership experience.</p>
        <label>Username<input name="username" autoComplete="username" required maxLength="150" value={form.username} onChange={update} /></label>
        <div className="input-row">
          <label>First Name<input name="first_name" autoComplete="given-name" required value={form.first_name} onChange={update} /></label>
          <label>Last Name<input name="last_name" autoComplete="family-name" required value={form.last_name} onChange={update} /></label>
        </div>
        <label>Email<input name="email" type="email" autoComplete="email" required value={form.email} onChange={update} /></label>
        <label>Password<input name="password" type="password" autoComplete="new-password" minLength="8" required value={form.password} onChange={update} /></label>
        {error && <p className="notice error">{error}</p>}
        <button className="button full-width" type="submit">Register</button>
        <p className="form-foot">Already have an account? <Link to="/login">Log in</Link></p>
      </form>
    </main>
  );
}
