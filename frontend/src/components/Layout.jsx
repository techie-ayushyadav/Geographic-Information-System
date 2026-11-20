import { useEffect, useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import api from "../api";
import { NAV } from "../nav";
import { GroupContext } from "../GroupContext";

export default function Layout() {
  const nav = useNavigate();
  const [groups, setGroups] = useState([]);
  const [groupId, setGroupId] = useState(null);
  const [stats, setStats] = useState({ assets: 0 });
  const [q, setQ] = useState("");
  const [results, setResults] = useState(null);

  useEffect(() => {
    api.get("/auth/groups").then(({ data }) => {
      setGroups(data);
      if (data.length) setGroupId(data[0].id);
    });
  }, []);

  useEffect(() => {
    if (groupId) api.get("/stats", { params: { group_id: groupId } }).then(({ data }) => setStats(data));
  }, [groupId]);

  useEffect(() => {
    if (!q.trim() || !groupId) return setResults(null);
    const t = setTimeout(() => {
      api.get("/search", { params: { q, group_id: groupId } }).then(({ data }) => setResults(data));
    }, 250);
    return () => clearTimeout(t);
  }, [q, groupId]);

  function logout() {
    localStorage.clear();
    nav("/login");
  }

  return (
    <GroupContext.Provider value={{ groupId }}>
      <header className="topbar">
        <div className="brand-sm"><span>GIS</span></div>
        <label className="group">
          Group
          <select value={groupId ?? ""} onChange={(e) => setGroupId(Number(e.target.value))}>
            {groups.map((g) => <option key={g.id} value={g.id}>{g.name}</option>)}
          </select>
        </label>
        <div className="search">
          <input placeholder="Search asset, customer, cable, OLT, ONT..." value={q}
                 onChange={(e) => setQ(e.target.value)} />
          {results && (
            <div className="search-results">
              {[...results.assets.map((a) => `${a.type} · ${a.name}`),
                ...results.cables.map((c) => `Cable · ${c.name}`),
                ...results.customers.map((c) => `Customer · ${c.name} (${c.code})`)]
                .map((t, i) => <div key={i}>{t}</div>)}
              {!results.assets.length && !results.cables.length && !results.customers.length &&
                <div className="muted">No results</div>}
            </div>
          )}
        </div>
        <div className="status"><span className="dot" /> Network Online <b>{stats.assets} assets</b></div>
        <div className="user">
          <strong>{localStorage.getItem("username")}</strong>
          <small>{localStorage.getItem("role")}</small>
        </div>
        <button className="logout" onClick={logout}>Logout</button>
      </header>

      <div className="shell">
        <aside className="sidebar">
          {NAV.map((s) => (
            <div key={s.section}>
              <div className="section">{s.section}</div>
              {s.items.map((i) => (
                <NavLink key={i.label} to={i.to} end className={({ isActive }) => (isActive ? "active" : "")}>
                  {i.label}
                </NavLink>
              ))}
            </div>
          ))}
        </aside>
        <main className="content"><Outlet /></main>
      </div>

      <footer>Geographic Information System (GIS)</footer>
    </GroupContext.Provider>
  );
}
