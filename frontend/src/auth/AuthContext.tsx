import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'
import { clearStoredToken, getStoredToken } from '@/api/auth'

type AuthContextValue = {
  loading: boolean
  authenticated: boolean
  refresh: () => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState(() => Boolean(getStoredToken()))
  const [authenticated, setAuthenticated] = useState(false)

  const verify = useCallback(async () => {
    const token = getStoredToken()
    if (!token) {
      setAuthenticated(false)
      setLoading(false)
      return
    }
    setLoading(true)
    try {
      const res = await fetch('/api/v1/auth/verify', {
        headers: { Authorization: `Bearer ${token}` },
      })
      const body = await res.json().catch(() => ({}))
      const ok =
        res.ok &&
        body &&
        typeof body === 'object' &&
        'valid' in body &&
        Boolean((body as { valid?: boolean }).valid)
      if (ok) {
        setAuthenticated(true)
      } else {
        if (res.status === 401) clearStoredToken()
        setAuthenticated(false)
      }
    } catch {
      setAuthenticated(false)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void verify()
  }, [verify])

  const refresh = useCallback(() => {
    void verify()
  }, [verify])

  const logout = useCallback(() => {
    clearStoredToken()
    setAuthenticated(false)
    setLoading(false)
  }, [])

  return (
    <AuthContext.Provider
      value={{ loading, authenticated, refresh, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const v = useContext(AuthContext)
  if (!v) throw new Error('useAuth 必须在 AuthProvider 内使用')
  return v
}
