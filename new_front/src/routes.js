import { Routes, Route, useParams } from 'react-router-dom';
// layouts
import DashboardLayout from './layouts/dashboard';
import SimpleLayout from './layouts/simple';
//
import BlogPage from './pages/BlogPage';
import UserPage from './pages/UserPage';
import LoginPage from './pages/LoginPage';
import Page404 from './pages/Page404';
import ProductsPage from './pages/ProductsPage';
import DashboardAppPage from './pages/DashboardAppPage';
import AddStages from './pages/AddStages';
import ProfilePage from './pages/Candidtate';

// ----------------------------------------------------------------------

function Candidate() {
  const params = useParams();
  return (
    <ProfilePage email={params.email} />
  );
}

export default function Router() {
  return (
  <Routes>
      <Route path='/candidate' element={<DashboardLayout />}>
        <Route path=":email" element={<Candidate />} />
    </Route>
    <Route path="/" element={<DashboardLayout />}>
        <Route path="candidates" element={<UserPage />} />
      <Route path="stages" element={<AddStages />} />
    </Route>
  </Routes>);
  // const routes = useRoutes([
  //   {
  //     path: '/',
  //     element: <DashboardLayout />,
  //     children: [
  //       { element: <Navigate to="/app" />, index: true },
  //       { path: 'app', element: <DashboardAppPage /> },
  //       { path: 'candidates', element: <UserPage /> },
  //       {
  //         path: 'candidate/:email',
  //         element: <ProfilePage />,
  //       },
  //       { path: 'stages', element: <AddStages /> },
  //       { path: 'blog', element: <BlogPage /> },
  //     ],
  //   },
  //   {
  //     path: 'login',
  //     element: <LoginPage />,
  //   },
  //   {
  //     element: <SimpleLayout />,
  //     children: [
  //       { element: <Navigate to="/dashboard/app" />, index: true },
  //       { path: '404', element: <Page404 /> },
  //       { path: '*', element: <Navigate to="/404" /> },
  //     ],
  //   },
  //   {
  //     path: '*',
  //     element: <Navigate to="/404" replace />,
  //   },
  // ]);

  // return routes;
}
