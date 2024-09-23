import * as React from "react";
import App from './App.jsx';
import Home from './Home.jsx';
import * as ReactDOM from "react-dom/client";
import ConnectionPage from "./ConnectionPage.jsx";
import Register from "./Register.jsx";
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
    path: "Register",
    element: <Register />
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
