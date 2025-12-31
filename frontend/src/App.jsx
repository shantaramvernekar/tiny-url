import { useState } from "react";

const defaultState = {
  longUrl: "",
  shortCode: "",
  result: null,
  message: "",
  loading: false,
};

const apiBase = import.meta.env.VITE_API_BASE || "";

async function handleResponse(response) {
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = payload.detail || "Unexpected error";
    throw new Error(detail);
  }
  return payload;
}

export default function App() {
  const [state, setState] = useState(defaultState);

  const updateState = (updates) => {
    setState((prev) => ({ ...prev, ...updates }));
  };

  const onCreate = async (event) => {
    event.preventDefault();
    updateState({ loading: true, message: "", result: null });
    try {
      const response = await fetch(`${apiBase}/api/urls`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ long_url: state.longUrl }),
      });
      const payload = await handleResponse(response);
      updateState({ result: payload, message: "Short URL created!" });
    } catch (error) {
      updateState({ message: error.message });
    } finally {
      updateState({ loading: false });
    }
  };

  const onLookup = async () => {
    updateState({ loading: true, message: "", result: null });
    try {
      const response = await fetch(`${apiBase}/api/urls/${state.shortCode}`);
      const payload = await handleResponse(response);
      updateState({ result: payload, message: "Loaded short URL details." });
    } catch (error) {
      updateState({ message: error.message });
    } finally {
      updateState({ loading: false });
    }
  };

  const onUpdateStatus = async (action) => {
    updateState({ loading: true, message: "", result: null });
    try {
      const response = await fetch(
        `${apiBase}/api/urls/${state.shortCode}/${action}`,
        { method: "PATCH" },
      );
      const payload = await handleResponse(response);
      updateState({
        result: payload,
        message: `Short URL ${action}d successfully.`,
      });
    } catch (error) {
      updateState({ message: error.message });
    } finally {
      updateState({ loading: false });
    }
  };

  const onDelete = async () => {
    updateState({ loading: true, message: "", result: null });
    try {
      const response = await fetch(`${apiBase}/api/urls/${state.shortCode}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail || "Unexpected error");
      }
      updateState({
        message: "Short URL deleted successfully.",
        result: null,
      });
    } catch (error) {
      updateState({ message: error.message });
    } finally {
      updateState({ loading: false });
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Tiny URL</h1>
        <p>Generate, manage, and redirect your short links.</p>
      </header>

      <section className="card">
        <h2>Create a short URL</h2>
        <form onSubmit={onCreate} className="stack">
          <label>
            Long URL
            <input
              type="url"
              placeholder="https://example.com/very/long/link"
              value={state.longUrl}
              onChange={(event) => updateState({ longUrl: event.target.value })}
              required
            />
          </label>
          <button type="submit" disabled={state.loading}>
            {state.loading ? "Working..." : "Generate short URL"}
          </button>
        </form>
      </section>

      <section className="card">
        <h2>Manage a short URL</h2>
        <div className="stack">
          <label>
            Short code
            <input
              type="text"
              placeholder="abc123"
              value={state.shortCode}
              onChange={(event) =>
                updateState({ shortCode: event.target.value })
              }
            />
          </label>
          <div className="button-row">
            <button onClick={onLookup} disabled={state.loading}>
              Load details
            </button>
            <button
              onClick={() => onUpdateStatus("activate")}
              disabled={state.loading}
            >
              Activate
            </button>
            <button
              onClick={() => onUpdateStatus("deactivate")}
              disabled={state.loading}
            >
              Deactivate
            </button>
            <button className="danger" onClick={onDelete} disabled={state.loading}>
              Delete
            </button>
          </div>
        </div>
      </section>

      {state.message && <div className="message">{state.message}</div>}

      {state.result && (
        <section className="card result">
          <h3>Short URL Details</h3>
          <dl>
            <div>
              <dt>Short URL</dt>
              <dd>
                <a href={state.result.short_url} target="_blank" rel="noreferrer">
                  {state.result.short_url}
                </a>
              </dd>
            </div>
            <div>
              <dt>Long URL</dt>
              <dd>{state.result.long_url}</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{state.result.active ? "Active" : "Inactive"}</dd>
            </div>
            <div>
              <dt>Created</dt>
              <dd>{new Date(state.result.created_at).toLocaleString()}</dd>
            </div>
          </dl>
        </section>
      )}
    </div>
  );
}
