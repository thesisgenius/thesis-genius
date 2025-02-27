// frontend/src/main.jsx
import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import App from "./App";
import AuthProvider from "./context/AuthProvider";
import ThesisProvider from "./context/ThesisProvider";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./index.css";

import NotFound from "./pages/NotFound";
import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import ManageThesis from "./pages/ManageThesis";
import Forum from "./pages/Forum";
import ProtectedRoute from "./components/ProtectedRoute";
import Part from "./pages/Part";
import About from "./pages/About";
import ThesisBody from "./pages/ThesisBody";
import MainApp from "./pages/MainApp";
import ProfilePage from "./pages/Profile";

// Constants for paths and routes
const ROUTES = {
  ROOT: "/",
  SIGNIN: "/signin",
  SIGNUP: "/signup",
  APP: "/app",
  ABOUT: "/about",
  DASHBOARD: "/dashboard",
  MANAGE_THESES: "manage-theses",
  MANAGE_FORUMS: "manage-forums",
  PROFILE: "profile",
};

const PART_ROUTES = [
  { path: "title", headerText: "Title Page", placeholder: "Title page..." },
  { path: "copyright", headerText: "Copyright Page", placeholder: "..." },
  { path: "signature", headerText: "Signature Page", placeholder: "..." },
  { path: "abstract", headerText: "Abstract Page", placeholder: "..." },
  { path: "dedication", headerText: "Dedication Page", placeholder: "..." },
  {
    path: "table-of-contents",
    headerText: "Table of Contents Page",
    placeholder: "...",
  },
  {
    path: "list-of-figures",
    headerText: "List of Figures Page",
    placeholder: "...",
  },
  {
    path: "list-of-tables",
    headerText: "List of Tables Page",
    placeholder: "...",
  },
  { path: "appendices", headerText: "Appendices Page", placeholder: "..." },
  { path: "references", headerText: "References Page", placeholder: "..." },
  { path: "other-info", headerText: "Other Info Page", placeholder: "..." },
];

// Simple wrapper for protected routes
export function ProtectedPage({ children }) {
  return <ProtectedRoute>{children}</ProtectedRoute>;
}

export function MainRoot() {
  // Hooks must be inside a component, not in the top-level module scope:
  const [refreshCount, setRefreshCount] = useState(0);

  function incrementRefreshCount() {
    setRefreshCount((prev) => prev + 1);
  }

  // Build the router with nested routes
  const router = createBrowserRouter([
    {
      path: ROUTES.ROOT,
      element: (
        <AuthProvider refreshApp={incrementRefreshCount}>
          <ThesisProvider>
            {/* Re-render <App> whenever refreshCount changes */}
            <App key={refreshCount} />
          </ThesisProvider>
        </AuthProvider>
      ),
      errorElement: <NotFound />,
      children: [
        // Public routes
        { path: ROUTES.ROOT, element: <Home /> },
        { path: ROUTES.SIGNIN, element: <SignIn /> },
        { path: ROUTES.SIGNUP, element: <SignUp /> },
        { path: ROUTES.ABOUT, element: <About /> },

        // The main "app" routes
        {
          path: ROUTES.APP,
          element: <MainApp />,
          children: [
            {
              path: ROUTES.PROFILE,
              element: (
                <ProtectedPage>
                  <ProfilePage />
                </ProtectedPage>
              ),
            },
            {
              path: ":thesisId/thesis-body",
              element: (
                <ProtectedPage>
                  <ThesisBody />
                </ProtectedPage>
              ),
            },
            ...PART_ROUTES.map(({ path, headerText, placeholder }) => ({
              path: `:thesisId/${path}`,
              element: (
                <ProtectedPage>
                  <Part
                    headerText={headerText}
                    textAreaPlaceholder={placeholder}
                  />
                </ProtectedPage>
              ),
            })),
            {
              path: ROUTES.MANAGE_THESES,
              element: (
                <ProtectedPage>
                  <ManageThesis />
                </ProtectedPage>
              ),
            },
            {
              path: ROUTES.MANAGE_FORUMS,
              element: (
                <ProtectedPage>
                  <Forum />
                </ProtectedPage>
              ),
            },
          ],
        },

        // Additional “dashboard” route
        {
          path: ROUTES.DASHBOARD,
          element: (
            <ProtectedPage>
              <ManageThesis />
            </ProtectedPage>
          ),
        },
      ],
    },
  ]);

  // Return the router
  return <RouterProvider router={router} />;
}

// Finally, render <MainRoot>:
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <MainRoot />
  </React.StrictMode>,
);
