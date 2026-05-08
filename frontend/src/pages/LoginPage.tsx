import { Redirect, useLocation } from 'wouter'
import { useAuth } from '@/auth/AuthContext'
import { LoginForm } from '@/components/LoginForm'
import '@/App.css'

export function LoginPage() {
  const [, setLocation] = useLocation()
  const { loading, authenticated, refresh } = useAuth()

  if (!loading && authenticated) {
    return <Redirect to="/app/projects" />
  }

  return (
    <div className="login-shell">
      <div className="login-card">
        <LoginForm
          onSuccess={() => {
            refresh()
            setLocation('/app/projects')
          }}
        />
      </div>
    </div>
  )
}
