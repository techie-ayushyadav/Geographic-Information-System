import { Navigate, Route, Routes } from "react-router-dom";
import Login from "./pages/Login.jsx";
import Layout from "./components/Layout.jsx";
import MapView from "./pages/MapView.jsx";
import AssetList from "./pages/AssetList.jsx";

const isAuthed = () => !!localStorage.getItem("token");

function Protected({ children }) {
  return isAuthed() ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <Protected>
            <Layout />
          </Protected>
        }
      >
        <Route index element={<MapView />} />
        <Route path="assets/:type" element={<AssetList />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
