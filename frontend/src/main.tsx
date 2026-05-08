import { createRoot } from 'react-dom/client'
import './index.css'
import { AuthProvider } from '@/auth/AuthContext'
import { AppRoutes } from '@/routes/AppRoutes'

createRoot(document.getElementById('root')!).render(
  <AuthProvider>
    <AppRoutes />
  </AuthProvider>,
)
