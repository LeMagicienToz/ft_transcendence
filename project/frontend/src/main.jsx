import * as React from "react";
import App from './App.jsx';
import Home from './Home.jsx';
import * as ReactDOM from "react-dom/client";
import ConnectionPage from "./ConnectionPage.jsx";
import Switch_button from "./log.jsx";
import Show_Avatar from "./avatar/AstronautAvatar.jsx";
import Code_sender from  "./42log.jsx";
import Homepage from "./Home/Homepage.jsx";

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
    path: "uWu",
    element: <ConnectionPage />,
  },
  {
    path: "Home",
    element: <Home />,
  },
  {
    path: "login",
    element: <Switch_button />,
  },
  {
    path: "login_42",
    element: <Code_sender />,
  },
  {
    path: "Homepage",
    element: <Homepage />,
  },
  {
    path: "Avatar",
    element: <Show_Avatar />,
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
);
