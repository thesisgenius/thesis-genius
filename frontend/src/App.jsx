import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Header from "./components/Header";
import Home from "./pages/Home";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp.jsx";
import Dashboard from "./pages/Dashboard";
import ThesisDashboard from "./pages/ThesisDashboard";
import ForumDashboard from "./pages/ForumDashboard";
import ForumPostEdit from "./components/ForumPostEdit";
import ForumPostView from "./components/ForumPostView";
import ForumPost from "./components/ForumPost";
import NotFound from "./pages/NotFound";
import Footer from "./components/Footer";
import NewDashBoard from "./pages/NewDashBoard";
import Dash from "./pages/Dash.jsx";
import Body from "./pages/Body";
import Part from "./pages/Part";

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
    NOT_FOUND: "*",
    // Workflow Thesis Pages
    NEW_DASHBOARD: "/dashboard/new",
    DASH: "/dashboard/:dashboardId",
    BODY: "/dashboard/:dashboardId/body",
    TITLE_PAGE: {
        PATH: "/thesis/:thesisId/title",
        HEADER: "Title Page",
        TEXTAREA: "Enter your title page content..."
    },
    ABSTRACT_PAGE: {
        PATH: "/thesis/:thesisId/abstract",
        HEADER: "Abstract Page",
        TEXTAREA: "Enter your abstract page content..."
    },
    TABLE_OF_CONTENTS_PAGE: {
        PATH: "/thesis/:thesisId/table-of-contents",
        HEADER: "Table of Contents Page",
        TEXTAREA: "Enter your table of contents page content..."
    },
    LIST_OF_FIGURES_PAGE: {
        PATH: "/thesis/:thesisId/list-of-figures",
        HEADER: "List of Figures Page",
        TEXTAREA: "Enter your list of figures page content..."
    },
    LIST_OF_TABLES_PAGE: {
        PATH: "/thesis/:thesisId/list-of-tables",
        HEADER: "List of Tables Page",
        TEXTAREA: "Enter your list of tables page content..."
    },
    APPENDICES_PAGE: {
        PATH: "/thesis/:thesisId/appendices",
        HEADER: "Appendices Page",
        TEXTAREA: "Enter your appendices page content..."
    },
    REFERENCES_PAGE: {
        PATH: "/thesis/:thesisId/references",
        HEADER: "References Page",
        TEXTAREA: "Enter your references page content..."
    }
};

// Extract routes into a separate function to make the component cleaner
const renderRoutes = () => (
    <Routes>
        <Route path={ROUTES.HOME} element={<Home />} />
        <Route path={ROUTES.SIGN_IN} element={<SignIn />} />
        <Route path={ROUTES.SIGN_UP} element={<SignUp />} />
        <Route path={ROUTES.DASHBOARD} element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path={ROUTES.NEW_DASHBOARD} element={<ProtectedRoute><NewDashBoard /></ProtectedRoute>} />
        <Route path={ROUTES.DASH} element={<ProtectedRoute><Dash /></ProtectedRoute>} />
        <Route path={ROUTES.BODY} element={<ProtectedRoute><Body /></ProtectedRoute>} />
        <Route path={ROUTES.THESIS} element={<ProtectedRoute><ThesisDashboard /></ProtectedRoute>} />
        <Route path={ROUTES.TITLE_PAGE.PATH} element={<ProtectedRoute><Part
            headerText={ROUTES.TITLE_PAGE.HEADER}
            textAreaPlaceholder={ROUTES.TITLE_PAGE.TEXTAREA}/>
        </ProtectedRoute>}
        />
        <Route path={ROUTES.ABSTRACT_PAGE.PATH} element={<ProtectedRoute><Part
            headerText={ROUTES.ABSTRACT_PAGE.HEADER}
            textAreaPlaceholder={ROUTES.ABSTRACT_PAGE.TEXTAREA}/>
        </ProtectedRoute>}
        />
        <Route path={ROUTES.TABLE_OF_CONTENTS_PAGE.PATH} element={<ProtectedRoute><Part
            headerText={ROUTES.TABLE_OF_CONTENTS_PAGE.HEADER}
            textAreaPlaceholder={ROUTES.TABLE_OF_CONTENTS_PAGE.TEXTAREA}/>
        </ProtectedRoute>}
        />
        <Route path={ROUTES.LIST_OF_FIGURES_PAGE.PATH} element={<ProtectedRoute><Part
            headerText={ROUTES.LIST_OF_FIGURES_PAGE.HEADER}
            textAreaPlaceholder={ROUTES.LIST_OF_FIGURES_PAGE.TEXTAREA}/>
        </ProtectedRoute>}
        />
        <Route path={ROUTES.LIST_OF_TABLES_PAGE.PATH} element={<ProtectedRoute><Part
            headerText={ROUTES.LIST_OF_TABLES_PAGE.HEADER}
            textAreaPlaceholder={ROUTES.LIST_OF_TABLES_PAGE.TEXTAREA}/>
            </ProtectedRoute>}
        />
        <Route path={ROUTES.APPENDICES_PAGE.PATH} element={<ProtectedRoute><Part
            headerText={ROUTES.APPENDICES_PAGE.HEADER}
            textAreaPlaceholder={ROUTES.APPENDICES_PAGE.TEXTAREA}/>
            </ProtectedRoute>}
        />
        <Route path={ROUTES.REFERENCES_PAGE.PATH} element={<ProtectedRoute><Part
            headerText={ROUTES.REFERENCES_PAGE.HEADER}
            textAreaPlaceholder={ROUTES.REFERENCES_PAGE.TEXTAREA}/>
        </ProtectedRoute>}
        />
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