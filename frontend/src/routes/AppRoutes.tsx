import React, { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from '../pages/Login';
import Register from '../pages/Register';
import ParentDashboard from '../pages/ParentDashboard';
import ChildDashboard from '../pages/ChildDashboard';
import { AuthContext } from '../contexts/AuthContext';

const AppRoutes = () => {
  const { user } = useContext(AuthContext)!;

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    );
  }

  return (
    <Routes>
      {user.role === 'parent' && (
        <Route path="/parent-dashboard" element={<ParentDashboard />} />
      )}
      {user.role === 'child' && (
        <Route path="/child-dashboard" element={<ChildDashboard />} />
      )}
      <Route path="*" element={<Navigate to={user.role === 'parent' ? '/parent-dashboard' : '/child-dashboard'} />} />
    </Routes>
  );
};

export default AppRoutes;
