import { type SubmitEvent, useState } from 'react'
import { loginWithPassword, setStoredToken } from '@/api/auth'

type Props = {
  onSuccess: () => void
}

export function LoginForm({ onSuccess }: Props) {
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const { access_token } = await loginWithPassword(username, password)
      setStoredToken(access_token)
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : '登录失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="login-form" onSubmit={onSubmit} noValidate>
      <h1 className="login-title">SceneWeave</h1>
      <p className="login-subtitle">使用管理员账号登录</p>

      <label className="login-field">
        <span>用户名</span>
        <input
          name="username"
          type="text"
          autoComplete="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          disabled={loading}
        />
      </label>

      <label className="login-field">
        <span>密码</span>
        <input
          name="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={loading}
        />
      </label>

      {error ? (
        <p className="login-error" role="alert">
          {error}
        </p>
      ) : null}

      <button type="submit" className="login-submit" disabled={loading}>
        {loading ? '登录中…' : '登录'}
      </button>

      <p className="login-hint">
        默认用户名为 <code>admin</code>，密码见项目根目录{' '}
        <code>.env</code> 中的 <code>AUTH_PASSWORD</code>。
      </p>
    </form>
  )
}
