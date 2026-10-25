import { useEffect, useState } from "react";
import { Link, NavLink, Route, Routes, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api } from "./api";
import Register from "../../../server/frontend/src/components/Register/Register.jsx";

function Header({ user, onLogout }) {
  return (
    <header className="topbar">
      <Link className="brand" to="/"><span className="brand-mark">C</span> Cars Dealership</Link>
      <nav className="nav">
        <NavLink to="/" end>Find a dealer</NavLink>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
      </nav>
      <div className="account">
        {user ? <><span className="welcome">Hi, {user}</span><button className="button button-quiet" onClick={onLogout}>Log out</button></> :
          <><Link className="login-link" to="/login">Log in</Link><Link className="button button-small" to="/register">Create account</Link></>}
      </div>
    </header>
  );
}

function DealerCard({ dealer, user }) {
  return (
    <article className="dealer-card">
      <div className="dealer-image" style={{ backgroundImage: dealer.image_url ? `url("${dealer.image_url}")` : undefined }}>
        <span className="image-label">Verified dealer</span>
      </div>
      <div className="dealer-card-content">
        <p className="eyebrow">{dealer.city}, {dealer.state}</p>
        <h2>{dealer.name}</h2>
        <p className="muted">{dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}</p>
        <p className="dealer-phone">{dealer.phone}</p>
        <div className="card-links">
          <Link className="text-link" to={`/dealers/${dealer.id}`}>View dealer &amp; reviews <span aria-hidden="true">→</span></Link>
          {user && <Link className="text-link" to={`/dealers/${dealer.id}/review`}>Review Dealer</Link>}
        </div>
      </div>
    </article>
  );
}

function HomePage({ user }) {
  const [dealers, setDealers] = useState([]);
  const [searchParams, setSearchParams] = useSearchParams();
  const state = searchParams.get("state") || "";
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    api(`/dealers/${state ? `?state=${encodeURIComponent(state)}` : ""}`)
      .then(setDealers)
      .catch((problem) => setError(problem.message))
      .finally(() => setLoading(false));
  }, [state]);

  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <p className="eyebrow eyebrow-light">YOUR NEXT DRIVE STARTS HERE</p>
          <h1>Find a dealership<br />you can feel good about.</h1>
          <p>Explore trusted local dealers, read real customer reviews, and make your next move with confidence.</p>
          <a className="button button-light" href="#dealers">Explore dealerships <span aria-hidden="true">↓</span></a>
        </div>
        <div className="hero-art" aria-hidden="true"><div className="sun"></div><div className="road"></div><div className="car-shape">✦</div></div>
      </section>
      <main className="content" id="dealers">
        <div className="section-heading">
          <div><p className="eyebrow">A better way to shop</p><h2>Dealerships near you</h2><p className="muted">Browse our growing nationwide network.</p></div>
          <label className="filter-label">Filter by state
            <select value={state} onChange={(event) => setSearchParams(event.target.value ? { state: event.target.value } : {})}>
              <option value="">All states</option><option value="KS">Kansas (KS)</option><option value="TX">Texas (TX)</option><option value="IL">Illinois (IL)</option><option value="WA">Washington (WA)</option>
            </select>
          </label>
        </div>
        {error && <p className="notice error">{error}</p>}
        {loading ? <p className="muted">Loading dealerships…</p> :
          dealers.length ? <div className="dealer-grid">{dealers.map((dealer) => <DealerCard key={dealer.id} dealer={dealer} user={user} />)}</div> :
            <div className="empty-state">No dealers found for this state yet.</div>}
      </main>
    </>
  );
}

function DealerPage({ user }) {
  const { dealerId } = useParams();
  const navigate = useNavigate();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState("");
  useEffect(() => {
    Promise.all([api(`/dealers/${dealerId}/`), api(`/dealers/${dealerId}/reviews/`)])
      .then(([dealerResult, reviewResult]) => { setDealer(dealerResult); setReviews(reviewResult); })
      .catch((problem) => setError(problem.message));
  }, [dealerId]);

  if (error) return <main className="content"><p className="notice error">{error}</p><Link to="/">Back to dealers</Link></main>;
  if (!dealer) return <main className="content muted">Loading dealership…</main>;
  const average = reviews.length ? (reviews.reduce((sum, item) => sum + item.rating, 0) / reviews.length).toFixed(1) : "New";
  return (
    <main className="content detail-layout">
      <Link className="back-link" to="/">← All dealerships</Link>
      <section className="detail-hero">
        <div className="detail-photo" style={{ backgroundImage: dealer.image_url ? `url("${dealer.image_url}")` : undefined }} />
        <div className="detail-copy"><p className="eyebrow">{dealer.city}, {dealer.state}</p><h1>{dealer.name}</h1><p className="muted">{dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}</p><p className="muted">{dealer.phone}</p><div className="rating-line"><span className="stars">★★★★★</span><b>{average}</b><span className="muted">({reviews.length} reviews)</span></div>
          {user ? <button className="button" onClick={() => navigate(`/dealers/${dealer.id}/review`)}>Review this dealer</button> : <p className="muted"><Link to="/login">Log in</Link> to share your experience.</p>}
        </div>
      </section>
      <section className="reviews-section"><div className="section-heading"><div><p className="eyebrow">Customer stories</p><h2>Reviews</h2></div>{user && <button className="button button-outline" onClick={() => navigate(`/dealers/${dealer.id}/review`)}>Write a review</button>}</div>
        {reviews.length ? <div className="review-list">{reviews.map((item) => <article className="review-card" key={item.id}><div className="review-top"><b>{item.username}</b><span className="stars">{"★".repeat(item.rating)}<span className="star-empty">{"★".repeat(5 - item.rating)}</span></span></div><p>{item.review}</p><small>{new Date(item.created_at).toLocaleDateString()}</small></article>)}</div> : <div className="empty-state">No reviews yet. Be the first to share your experience.</div>}
      </section>
    </main>
  );
}

function ReviewPage({ user }) {
  const { dealerId } = useParams();
  const navigate = useNavigate();
  const [rating, setRating] = useState(5);
  const [review, setReview] = useState("");
  const [sentiment, setSentiment] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api(`/dealers/${dealerId}/`).catch((problem) => setError(problem.message));
  }, [dealerId]);
  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      await api("/reviews/", { method: "POST", body: JSON.stringify({ dealer_id: Number(dealerId), rating, review }) });
      navigate(`/dealers/${dealerId}`, { state: { posted: true } });
    } catch (problem) { setError(problem.message); }
  }
  async function analyze() {
    try { setSentiment(await api("/analyze-review/", { method: "POST", body: JSON.stringify({ review }) })); }
    catch (problem) { setError(problem.message); }
  }
  if (!user) return <main className="form-page"><div className="form-card"><h1>Sign in to review</h1><p className="muted">Create an account or log in before posting a review.</p><Link className="button" to="/login">Log in</Link></div></main>;
  return (
    <main className="form-page"><form className="form-card" onSubmit={submit}>
      <Link className="back-link" to={`/dealers/${dealerId}`}>← Back to dealership</Link><p className="eyebrow">Your experience matters</p><h1>Write a review</h1><p className="muted">Posting as <strong>{user}</strong></p>
      <label>Rating <select value={rating} onChange={(event) => setRating(Number(event.target.value))}><option value="5">5 — Excellent</option><option value="4">4 — Great</option><option value="3">3 — Good</option><option value="2">2 — Fair</option><option value="1">1 — Poor</option></select></label>
      <label>Your review <textarea required minLength="1" maxLength="2000" rows="6" value={review} onChange={(event) => { setReview(event.target.value); setSentiment(null); }} placeholder="What should other drivers know?" /></label>
      <div className="form-actions"><button className="button button-outline" type="button" disabled={!review.trim()} onClick={analyze}>Check sentiment</button><button className="button" type="submit">Post review</button></div>
      {sentiment && <p className="sentiment">Sentiment: <b>{sentiment.label}</b> (score {sentiment.score})</p>}
      {error && <p className="notice error">{error}</p>}
    </form></main>
  );
}

function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  async function submit(event) {
    event.preventDefault();
    try { await api("/login/", { method: "POST", body: JSON.stringify({ username, password }) }); await onLogin(); navigate("/"); }
    catch (problem) { setError(problem.message); }
  }
  return <main className="form-page"><form className="form-card" onSubmit={submit}><p className="eyebrow">Welcome back</p><h1>Log in</h1><label>Username<input autoComplete="username" required value={username} onChange={(event) => setUsername(event.target.value)} /></label><label>Password<input type="password" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} /></label>{error && <p className="notice error">{error}</p>}<button className="button full-width">Log in</button><p className="form-foot">New here? <Link to="/register">Create an account</Link></p></form></main>;
}

function RegisterPage({ onLogin }) {
  const navigate = useNavigate();
  return <Register onRegistered={async () => { await onLogin(); navigate("/"); }} />;
}

export default function App() {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  async function refreshUser() {
    try { const session = await api("/me/"); setUser(session.authenticated ? session.username : null); }
    catch { setUser(null); }
    finally { setReady(true); }
  }
  useEffect(() => { refreshUser(); }, []);
  async function logoutUser() {
    try { await api("/logout/", { method: "POST", body: "{}" }); setUser(null); }
    catch (problem) { window.alert(problem.message); }
  }
  if (!ready) return <div className="loading-screen">Cars Dealership</div>;
  return <><Header user={user} onLogout={logoutUser} /><Routes>
    <Route path="/" element={<HomePage user={user} />} />
    <Route path="/dealers/:dealerId" element={<DealerPage user={user} />} />
    <Route path="/dealers/:dealerId/review" element={<ReviewPage user={user} />} />
    <Route path="/login" element={<LoginPage onLogin={refreshUser} />} />
    <Route path="/register" element={<RegisterPage onLogin={refreshUser} />} />
    <Route path="*" element={<main className="content"><h1>Page not found</h1><Link to="/">Browse dealerships</Link></main>} />
  </Routes><footer className="app-footer"><span>© {new Date().getFullYear()} Cars Dealership</span><span>Real reviews. Better road trips.</span></footer></>;
}
