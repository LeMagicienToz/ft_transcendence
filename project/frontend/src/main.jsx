import * as React from "react";
import App from './App.jsx';
import Home from './Home.jsx';
import * as ReactDOM from "react-dom/client";
import Switch_button from "./log.jsx";
import Show_Avatar from "./avatar/AstronautAvatar.jsx";
import Homepage from "./Home/Homepage.jsx";
import Profile from "./Home/Profile.jsx";

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
    path: "Home",
    element: <Home />,
  },
  {
    path: "login",
    element: <Switch_button />,
  },
  {
    path: "Homepage",
    element: <Homepage />,
  },
  {
    path: "Profile",
    element: <Profile />,
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
