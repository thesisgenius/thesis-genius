import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Header from "./components/Header";
import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import ThesisDashboard from "./pages/ThesisDashboard";
import ForumDashboard from "./pages/ForumDashboard";
import ForumPostEdit from "./components/ForumPostEdit";
import ForumPostView from "./components/ForumPostView";
import ForumPost from "./components/ForumPost";
import NotFound from "./pages/NotFound";
import Footer from "./components/Footer";

// Define route paths as constants for better clarity and reuse
const ROUTES = {
    HOME: "/",
    SIGN_IN: "/signin",
    SIGN_UP: "/signup",
    DASHBOARD: "/dashboard",
    THESIS: "/thesis/:thesisId",
    FORUM: "/forum",
    FORUM_POST: "/forum/posts/:postId",
    FORUM_NEW_POST: "/forum/posts/new",
    FORM_EDIT_POST: "/forum/posts/:postId/edit",
    NOT_FOUND: "*"
};

// Extract routes into a separate function to make the component cleaner
const renderRoutes = () => (
    <Routes>
        <Route path={ROUTES.HOME} element={<Home />} />
        <Route path={ROUTES.SIGN_IN} element={<SignIn />} />
        <Route path={ROUTES.SIGN_UP} element={<Signup />} />
        <Route path={ROUTES.DASHBOARD} element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path={ROUTES.THESIS} element={<ProtectedRoute><ThesisDashboard /></ProtectedRoute>} />
        <Route path={ROUTES.FORUM} element={<ProtectedRoute><ForumDashboard /></ProtectedRoute>} />
        <Route path={ROUTES.FORUM_POST} element={<ProtectedRoute><ForumPostView /></ProtectedRoute>} />
        <Route path={ROUTES.FORUM_NEW_POST} element={<ProtectedRoute><ForumPost /></ProtectedRoute>} />
        <Route path={ROUTES.FORM_EDIT_POST} element={<ForumPostEdit />} />
        <Route path={ROUTES.NOT_FOUND} element={<NotFound />} />
    </Routes>
);

const App = () => {
    return (
        <Router>
            <Header />
            {renderRoutes()}
            <Footer />
        </Router>
    );
};

export default App;