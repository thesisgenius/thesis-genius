import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './index.css';
import NotFound from './pages/NotFound';

import Home from './pages/Home';
import SignIn from './pages/SignIn';
import Signup from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import Thesis from './pages/Thesis';
import ThesisDashboard from './pages/ThesisDashboard';
import Forum from './pages/Forum';
import ProtectedRoute from './components/ProtectedRoute';
import NewDashBoard from './pages/NewDashBoard';
import Dash from './pages/Dash';
import Part from './pages/Part';
import About from './pages/About';
import ThesisBody from './pages/ThesisBody';
import DynamicPart from './pages/DynamicPart';
import MainApp from './pages/MainApp';
import ProfilePage from './pages/Profile';

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <AuthProvider>
        <App />
      </AuthProvider>
    ),
    errorElement: <NotFound />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/signin', element: <SignIn /> },
      { path: '/signup', element: <Signup /> },
      { path: '/about', element: <About /> },

      // App
      {
        path: '/app',
        element: <MainApp />,
        children: [
          {
            path: 'title',
            element: (
              <Part
                headerText='Title Page'
                textAreaPlaceholder='Enter your title page content...'
              />
            ),
          },
          {
            path: 'profile',
            element: <ProfilePage />,
          },
          {
            path: 'copyright',
            element: (
              <Part
                headerText='Copyright Page'
                textAreaPlaceholder='Enter your copyright page content...'
              />
            ),
          },
          {
            path: 'signature',
            element: (
              <Part
                headerText='Signature Page'
                textAreaPlaceholder='Enter your signature page content...'
              />
            ),
          },
          {
            path: 'abstract',
            element: (
              <Part
                headerText='Abstract Page'
                textAreaPlaceholder='Enter your abstract content...'
              />
            ),
          },
          {
            path: 'dedication',
            element: (
              <Part
                headerText='Dedication Page'
                textAreaPlaceholder='Enter your dedication page content...'
              />
            ),
          },
          {
            path: 'table-of-contents',
            element: (
              <Part
                headerText='Table of Contents Page'
                textAreaPlaceholder='Enter table of contents content...'
              />
            ),
          },
          {
            path: 'list-of-figures',
            element: (
              <Part
                headerText='List of Figures Page'
                textAreaPlaceholder='Enter list of figures content...'
              />
            ),
          },
          {
            path: 'list-of-tables',
            element: (
              <Part
                headerText='List of Tables Page'
                textAreaPlaceholder='Enter list of tables content...'
              />
            ),
          },
          {
            path: 'appendices',
            element: (
              <Part
                headerText='Appendices Page'
                textAreaPlaceholder='Enter appendices content...'
              />
            ),
          },
          {
            path: 'references',
            element: (
              <Part
                headerText='References Page'
                textAreaPlaceholder='Enter references content...'
              />
            ),
          },
          {
            path: 'other-info',
            element: (
              <Part
                headerText='Other Info Page'
                textAreaPlaceholder='Enter other information content...'
              />
            ),
          },

          // Other Parts
          { path: 'thesis-body', element: <ThesisBody /> },
          {
            path: 'manage-theses',
            element: (
              <ProtectedRoute>
                <Thesis />
              </ProtectedRoute>
            ),
          },
          {
            path: 'manage-forums',
            element: (
              <ProtectedRoute>
                <Forum />
              </ProtectedRoute>
            ),
          },
        ],
      },

      // { path: '/newdashboard', element: <NewDashBoard /> },
      // { path: '/body', element: <ThesisBody /> },
      // { path: '/dash', element: <Dash /> },
      // { path: '/dynamicpart', element: <DynamicPart /> },
      // {
      //   path: '/dashboard',
      //   element: (
      //     <ProtectedRoute>
      //       <Dashboard />
      //     </ProtectedRoute>
      //   ),
      // },

      // {
      //   path: '/thesis/:thesisId',
      //   element: (
      //     <ProtectedRoute>
      //       <ThesisDashboard />
      //     </ProtectedRoute>
      //   ),
      // },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
