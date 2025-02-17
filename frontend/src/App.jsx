import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import Thesis from "./pages/Thesis";
import ThesisDashboard from "./pages/ThesisDashboard";
import Forum from "./pages/Forum";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Part from "./pages/Part";
import About from "./pages/About";

const partRoutes = [
    { path: "/title", headerText: "Title Page", placeholder: "Enter your title page content..." },
    { path: "/copyright", headerText: "Copyright Page", placeholder: "Enter your copyright page content..." },
    { path: "/signature", headerText: "Signature Page", placeholder: "Enter your signature page content..." },
    { path: "/abstract", headerText: "Abstract Page", placeholder: "Enter your abstract content..." },
    { path: "/dedication", headerText: "Dedication Page", placeholder: "Enter your dedication page content..." },
    { path: "/table-of-contents", headerText: "Table of Contents Page", placeholder: "Enter table of contents content..." },
    { path: "/list-of-figures", headerText: "List of Figures Page", placeholder: "Enter list of figures content..." },
    { path: "/list-of-tables", headerText: "List of Tables Page", placeholder: "Enter list of tables content..." },
    { path: "/appendices", headerText: "Appendices Page", placeholder: "Enter appendices content..." },
    { path: "/references", headerText: "References Page", placeholder: "Enter references content..." },
    { path: "/other-info", headerText: "Other Info Page", placeholder: "Enter other information content..." },
];

const protectedRoutes = [
    { path: "/dashboard", element: <Dashboard /> },
    { path: "/thesis", element: <Thesis /> },
    { path: "/thesis/:thesisId", element: <ThesisDashboard /> },
    { path: "/forum", element: <Forum /> },
];

const App = () => {
    const renderProtectedRoute = (path, component) => (
        <Route
            key={path}
            path={path}
            element={<ProtectedRoute>{component}</ProtectedRoute>}
        />
    );

    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/signin" element={<SignIn />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/about" element={<About />} />
                {protectedRoutes.map(({ path, element }) => renderProtectedRoute(path, element))}
                {partRoutes.map(({ path, headerText, placeholder }) => (
                    <Route
                        key={path}
                        path={path}
                        element={<Part headerText={headerText} textAreaPlaceholder={placeholder} />}
                    />
                ))}
                <Route path="*" element={<NotFound />} />
            </Routes>
            <Footer />
        </Router>
    );
};

export default App;