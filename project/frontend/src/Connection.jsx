import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import ConnectionPage from './ConnectionPage.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ConnectionPage />
  </StrictMode>,
)
