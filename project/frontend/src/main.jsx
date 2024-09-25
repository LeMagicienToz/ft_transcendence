import * as React from "react";
import App from './App.jsx';
import Home from './Home.jsx';
import * as ReactDOM from "react-dom/client";
import ConnectionPage from "./ConnectionPage.jsx";
import Switch_button from "./log.jsx";
import AstronautAvatar from "./avatar/AstronautAvatar.jsx"
import SpaceBackground from './Theme/spacebg';

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "Login",
    element: <ConnectionPage />,
  },
  {
    path: "Home",
    element: <Home />,
  },
  {
    path: "Log",
    element: <Switch_button />,
  },
  {
    path: "Avatar",
    element: <AstronautAvatar />,
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <SpaceBackground>
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
  </SpaceBackground>
);
