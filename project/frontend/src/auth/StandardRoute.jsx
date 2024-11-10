import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const StandardRoute = () => {
  const { isAuthenticated, loading } = useContext(AuthContext);

  if (loading) {
    return ;
  }

  return isAuthenticated ? <Navigate to="/homepage" /> : <Outlet />;
};

export default StandardRoute;
