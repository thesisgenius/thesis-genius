// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useAuth } from "./context/AuthContext"; // ✅ Import the useAuth hook
import Home from "./pages/Home";
// Layout
import Header from "./components/Header";
import Footer from "./components/Footer";

// Pages
import AccountSettings from "./pages/AccountSettings";
import SignIn from "./pages/SignIn";
import Signup from "./pages/SignUp";
import About from "./pages/About";
import ContactUs from "./pages/ContactUs";
import ChatWindow from "./pages/ChatWindow";

import NotFound from "./pages/NotFound";

// Protected Pages
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import Thesis from "./pages/Thesis";
import ThesisDashboard from "./pages/ThesisDashboard";
import NewDashBoard from "./pages/NewDashBoard";
import Dash from "./pages/Dash";
import Body from "./pages/Body";
import ThesisBody from "./pages/ThesisBody";
import Part from "./pages/Part";
import DynamicPart from "./pages/DynamicPart";

const App = () => {
  const { user } = useAuth(); // ✅ Access the user state

  return (
    <Router>
      <Header />
      <Routes>
        {/* 🏠 Home Page (Conditional Rendering) */}
        <Route path="/" element={<Home />} />/{/* 📝 Public Routes */}
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<ContactUs />} />
        <Route path="/chat" element={<ChatWindow />} />
        {/* 🌐 External Pages */}
        {/* 🔒 Protected Routes */}
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
        {/* 📄 Additional Pages */}
        <Route path="/newdashboard" element={<NewDashBoard />} />
        <Route path="/dash" element={<Dash />} />
        <Route path="/body" element={<ThesisBody />} />
        <Route path="/thesisbody" element={<ThesisBody />} />
        <Route path="/part" element={<Part />} />
        <Route path="/account-settings" element={<AccountSettings />} />
        <Route path="/dynamicpart" element={<DynamicPart />} />
        {/* ⚠️ 404 - Catch-All */}
        <Route path="*" element={<NotFound />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
