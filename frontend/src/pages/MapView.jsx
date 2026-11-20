import { useEffect, useState } from "react";
import { CircleMarker, GeoJSON, MapContainer, Popup, TileLayer } from "react-leaflet";
import api from "../api";
import { useGroup } from "../GroupContext";

const COLORS = {
  OLT: "#7c4dff", ODF: "#f5b301", FAT: "#ffffff", SPLITTER: "#2ecc71",
  SPLICE_CLOSURE: "#e67e22", POLE: "#95a5a6", MANHOLE: "#7f8c8d", ONT: "#e74c3c",
};

export default function MapView() {
  const { groupId } = useGroup();
  const [features, setFeatures] = useState([]);

  useEffect(() => {
    if (!groupId) return;
    api.get("/map/features", { params: { group_id: groupId } }).then(({ data }) => setFeatures(data.features));
  }, [groupId]);

  const points = features.filter((f) => f.geometry.type === "Point");
  const lines = features.filter((f) => f.geometry.type === "LineString");

  return (
    <MapContainer center={[22.65, 75.85]} zoom={10} className="map">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {lines.map((f) => (
        <GeoJSON key={`c${f.properties.id}`} data={f} style={{ color: "#18b8ff", weight: 4 }}>
          <Popup>{f.properties.name} · {f.properties.core_count} cores</Popup>
        </GeoJSON>
      ))}
      {points.map((f) => {
        const [lng, lat] = f.geometry.coordinates;
        const color = COLORS[f.properties.asset_type] || "#3498db";
        return (
          <CircleMarker key={`a${f.properties.id}`} center={[lat, lng]} radius={8}
                        pathOptions={{ color: "#111", weight: 2, fillColor: color, fillOpacity: 1 }}>
            <Popup>
              <b>{f.properties.name}</b><br />
              {f.properties.asset_type} · {f.properties.status}
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
