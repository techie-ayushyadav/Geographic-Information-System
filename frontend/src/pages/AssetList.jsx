import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import { useGroup } from "../GroupContext";

export default function AssetList() {
  const { type } = useParams();
  const { groupId } = useGroup();
  const [rows, setRows] = useState([]);
  const [form, setForm] = useState({ name: "", lat: "", lng: "" });
  const canWrite = ["SUPER_ADMIN", "ADMIN", "EDITOR", "FIELD"].includes(localStorage.getItem("role"));

  const load = () =>
    groupId && api.get("/assets", { params: { group_id: groupId, asset_type: type } })
      .then(({ data }) => setRows(data));

  useEffect(() => { load(); }, [groupId, type]);

  async function add(e) {
    e.preventDefault();
    await api.post("/assets", {
      group_id: groupId, asset_type: type, name: form.name,
      lat: parseFloat(form.lat), lng: parseFloat(form.lng),
    });
    setForm({ name: "", lat: "", lng: "" });
    load();
  }

  return (
    <div className="page">
      <h2>{type.replaceAll("_", " ")}</h2>

      {canWrite && (
        <form className="inline-form" onSubmit={add}>
          <input placeholder="Name" value={form.name} required
                 onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Latitude" value={form.lat} required
                 onChange={(e) => setForm({ ...form, lat: e.target.value })} />
          <input placeholder="Longitude" value={form.lng} required
                 onChange={(e) => setForm({ ...form, lng: e.target.value })} />
          <button>+ Add</button>
        </form>
      )}

      <table>
        <thead><tr><th>ID</th><th>Name</th><th>Status</th><th>Lat</th><th>Lng</th></tr></thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}><td>{r.id}</td><td>{r.name}</td><td>{r.status}</td>
              <td>{r.lat.toFixed(5)}</td><td>{r.lng.toFixed(5)}</td></tr>
          ))}
          {!rows.length && <tr><td colSpan="5" className="muted">No records yet.</td></tr>}
        </tbody>
      </table>
    </div>
  );
}
