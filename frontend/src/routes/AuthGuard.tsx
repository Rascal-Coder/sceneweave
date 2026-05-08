import type { ReactNode } from 'react'
import { Redirect } from 'wouter'
import { useAuth } from '@/auth/AuthContext'

export function AuthGuard({ children }: { children: ReactNode }) {
  const { loading, authenticated } = useAuth()

  if (loading) {
    return (
      <div className="auth-fullscreen-loading" role="status" aria-live="polite">
        加载中…
      </div>
    )
  }

  if (!authenticated) {
    return <Redirect to="/login" />
  }

  return <>{children}</>
}
