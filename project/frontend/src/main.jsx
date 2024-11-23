import * as React from "react";
import App from './App.jsx';
import Home from './Home.jsx';
import * as ReactDOM from "react-dom/client";
import Switch_button from "./log.jsx";
import Show_Avatar from "./avatar/AstronautAvatar.jsx";
import Homepage from "./Home/Homepage.jsx";
import Profile from "./Home/Profile.jsx";
import WaitingRoom from "./game/WaitingRoom.jsx";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from './auth/AuthContext';
import StandardRoute from "./auth/StandardRoute.jsx";
import ProtectedRoute from "./auth/ProtectedRoute.jsx";
import { AuthWebSocketProvider } from './auth/AuthWebSocketContext.jsx';

const AppRouter = () => (
<AuthProvider>
    <Router>
      <Routes>
        <Route element={<StandardRoute />}>
          <Route path="/" element={<App />} />
          <Route path="/login" element={<Switch_button />} />
        </Route>
        <Route element={
          <AuthWebSocketProvider>
            <ProtectedRoute />
          </AuthWebSocketProvider>
          }>
          <Route path="/home" element={<Home />} />
          <Route path="/homepage" element={<Homepage />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/avatar" element={<Show_Avatar />} />
          {window.isDebug ? <Route path="/waitingroom" element={<GameDebug />} /> : <Route path="/waitingroom" element={<WaitingRoom />} />}
        </Route>
      </Routes>
    </Router>
</AuthProvider>
);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AppRouter />
  </React.StrictMode>
);
