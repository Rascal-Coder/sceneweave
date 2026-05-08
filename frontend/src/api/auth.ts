const TOKEN_KEY = 'sceneweave_access_token'

export type TokenResponse = {
  access_token: string
  token_type: string
}

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearStoredToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

/** POST OAuth2 password form to `/api/v1/auth/token` (Vite dev: proxied to backend). */
export async function loginWithPassword(
  username: string,
  password: string,
): Promise<TokenResponse> {
  const body = new URLSearchParams({
    username: username.trim(),
    password,
  })

  const res = await fetch('/api/v1/auth/token', {
    method: 'POST',
    body,
  })

  const data = (await res.json().catch(() => ({}))) as
    | TokenResponse
    | { detail?: string | unknown }

  if (!res.ok) {
    const detail =
      typeof data === 'object' &&
      data !== null &&
      'detail' in data &&
      typeof (data as { detail?: unknown }).detail === 'string'
        ? (data as { detail: string }).detail
        : res.statusText || '登录失败'
    throw new Error(detail)
  }

  const typed = data as TokenResponse
  if (!typed.access_token) {
    throw new Error('响应缺少 access_token')
  }
  return typed
}
