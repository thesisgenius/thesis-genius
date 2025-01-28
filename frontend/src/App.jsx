import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import Signup from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import Thesis from "./pages/Thesis";
import ThesisDashboard from "./pages/ThesisDashboard";
import Forum from "./pages/Forum";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import Header from "./components/Header";
import Footer from "./components/Footer";
import NewDashBoard from "./pages/NewDashBoard";
import Dash from "./pages/dash";
import Body from "./pages/Body";
import Part from "./pages/Part";

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/newdashboard" element={<NewDashBoard />} />
        <Route path="/body" element={<Body />} />
        <Route path="/dash" element={<Dash />} />
        <Route path="/part" element={<Part />} />
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
        <Route
          path="/title"
          element={
            <Part
              headerText="Title Page"
              textAreaPlaceholder="Enter your title page content..."
            />
          }
        />
        <Route
          path="/abstract"
          element={
            <Part
              headerText="Abstract Page"
              textAreaPlaceholder="Enter your abstract content..."
            />
          }
        />
        <Route
          path="/table-of-contents"
          element={
            <Part
              headerText="Table of Contents Page"
              textAreaPlaceholder="Enter table of contents content..."
            />
          }
        />
        <Route
          path="/list-of-figures"
          element={
            <Part
              headerText="List of Figures Page"
              textAreaPlaceholder="Enter list of figures content..."
            />
          }
        />
        <Route
          path="/list-of-tables"
          element={
            <Part
              headerText="List of Tables Page"
              textAreaPlaceholder="Enter list of tables content..."
            />
          }
        />
        <Route
          path="/appendices"
          element={
            <Part
              headerText="Appendices Page"
              textAreaPlaceholder="Enter appendices content..."
            />
          }
        />
        <Route
          path="/references"
          element={
            <Part
              headerText="References Page"
              textAreaPlaceholder="Enter references content..."
            />
          }
        />
        <Route
          path="/other-info"
          element={
            <Part
              headerText="Other Info Page"
              textAreaPlaceholder="Enter other information content..."
            />
          }
        />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
