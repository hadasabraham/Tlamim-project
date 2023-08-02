import { Routes, Route, useParams } from 'react-router-dom';
// layouts
import DashboardLayout from './layouts/dashboard';
import UserPage from './pages/UserPage';
import DashboardAppPage from './pages/DashboardAppPage';
import AddStages from './pages/AddStages';
import ProfilePage from './pages/Candidtate';
// import LoginPage from './pages/LoginPage';
import LoginPage from './layouts/dashboard/LoginPage';
// ----------------------------------------------------------------------

function Candidate() {
  const params = useParams();
  return (
    <ProfilePage email={params.email} />
  );
}

export default function Router() {
  return (
  <Routes path="/">
      <Route path="/" element={<DashboardLayout/>}>
        <Route path="/candidate/:email" element={<Candidate />} />
        <Route path="candidates" element={<UserPage />} />
        <Route path="stages" element={<AddStages />} />
        <Route path="statistics" element={<DashboardAppPage />} />
        <Route path="" element={<LoginPage/>} />
      </Route>
  </Routes>);
}
