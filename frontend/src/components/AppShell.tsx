import type { ReactNode } from 'react'
import { Link, useLocation } from 'wouter'
import { useAuth } from '@/auth/AuthContext'

type Props = {
  children: ReactNode
}

function NavLink({
  href,
  children,
}: {
  href: string
  children: ReactNode
}) {
  return (
    <Link
      href={href}
      className={(active) =>
        active ? 'app-nav-link is-active' : 'app-nav-link'
      }
    >
      {children}
    </Link>
  )
}

export function AppShell({ children }: Props) {
  const [, setLocation] = useLocation()
  const { logout } = useAuth()

  return (
    <div className="app-shell">
      <header className="app-shell-nav" aria-label="主导航">
        <span className="app-shell-brand">SceneWeave</span>
        <nav className="app-shell-links">
          <NavLink href="/app/projects">项目</NavLink>
          <NavLink href="/app/assets">素材库</NavLink>
          <NavLink href="/app/settings">系统配置</NavLink>
        </nav>
        <div className="app-shell-spacer" />
        <button
          type="button"
          className="app-nav-button"
          onClick={() => {
            logout()
            setLocation('/login')
          }}
        >
          退出登录
        </button>
      </header>
      {children}
    </div>
  )
}
