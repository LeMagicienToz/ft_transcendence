import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';          // Main App Component
import ConnectionPage from './ConnectionPage.jsx' // Other components

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <React.StrictMode>
     <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />        {/* Home route */}
      <Route path="/ConnectionPage" element={<ConnectionPage />} />  {/* About route */}
     </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
