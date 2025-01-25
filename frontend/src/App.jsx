import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Thesis from "./pages/Thesis";
import ThesisDashboard from "./pages/ThesisDashboard";
import Forum from "./pages/Forum";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import Header from "./components/Header";
import Footer from "./components/Footer";

const App = () => {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/signin" element={<SignIn />} />
                <Route path="/signup" element={<Signup />} />
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/thesis"
                    element={
                        <ProtectedRoute>
                            <Thesis />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/thesis/:thesisId"
                    element={
                        <ProtectedRoute>
                            <ThesisDashboard />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/forum"
                    element={
                        <ProtectedRoute>
                            <Forum />
                        </ProtectedRoute>
                    }
                />
                <Route path="*" element={<NotFound />} />
            </Routes>
            <Footer />
        </Router>
    );
};

export default App;
