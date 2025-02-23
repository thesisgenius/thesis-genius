import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./context/AuthContext";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./index.css";
import NotFound from "./pages/NotFound";

import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import Signup from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import ThesisDashboard from "./pages/ThesisDashboard";
import Forum from "./pages/Forum";
import ProtectedRoute from "./components/ProtectedRoute";
import Part from "./pages/Part";
import About from "./pages/About";
import ThesisBody from "./pages/ThesisBody";
import MainApp from "./pages/MainApp";
import ProfilePage from "./pages/Profile";

const partRoutes = [
    { path: "title", headerText: "Title Page", placeholder: "Enter your title page content..." },
    { path: "copyright", headerText: "Copyright Page", placeholder: "Enter your copyright page content..." },
    { path: "signature", headerText: "Signature Page", placeholder: "Enter your signature page content..." },
    { path: "abstract", headerText: "Abstract Page", placeholder: "Enter your abstract content..." },
    { path: "dedication", headerText: "Dedication Page", placeholder: "Enter your dedication page content..." },
    { path: "table-of-contents", headerText: "Table of Contents Page", placeholder: "Enter table of contents content..." },
    { path: "list-of-figures", headerText: "List of Figures Page", placeholder: "Enter list of figures content..." },
    { path: "list-of-tables", headerText: "List of Tables Page", placeholder: "Enter list of tables content..." },
    { path: "appendices", headerText: "Appendices Page", placeholder: "Enter appendices content..." },
    { path: "references", headerText: "References Page", placeholder: "Enter references content..." },
    { path: "other-info", headerText: "Other Info Page", placeholder: "Enter other information content..." },
];

const router = createBrowserRouter([
    {
        path: "/",
        element: (
            <AuthProvider>
                <App />
            </AuthProvider>
        ),
        errorElement: <NotFound />,
        children: [
            { path: "/", element: <Home /> },
            { path: "/signin", element: <SignIn /> },
            { path: "/signup", element: <Signup /> },
            { path: "/about", element: <About /> },

            {
                path: "/app",
                element: <MainApp />,
                children: [
                    { path: "profile", element: <ProtectedRoute><ProfilePage /></ProtectedRoute> },
                    ...partRoutes.map(({ path, headerText, placeholder }) => ({
                        path,
                        element: <Part headerText={headerText} textAreaPlaceholder={placeholder} />,
                    })),
                    { path: "thesis-body", element: <ThesisBody /> },
                    {
                        path: "manage-theses",
                        element: (
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        ),
                    },
                    {
                        path: "manage-forums",
                        element: (
                            <ProtectedRoute>
                                <Forum />
                            </ProtectedRoute>
                        ),
                    },
                ],
            },
            {
                path: "/dashboard",
                element: (
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                ),
            },
            {
                path: "/thesis/:thesisId",
                element: (
                    <ProtectedRoute>
                        <ThesisDashboard />
                    </ProtectedRoute>
                ),
            },
        ],
    },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);
