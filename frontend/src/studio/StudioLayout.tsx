import { useEffect, useState, type ReactNode } from 'react'
import { Link, useLocation, useParams } from 'wouter'
import { useAuth } from '@/auth/AuthContext'
import { ProjectStudioProvider } from '@/studio/ProjectStudioContext'
import { StudioCanvasRouter } from '@/studio/StudioCanvasRouter'

type ProjectPayload = {
  name: string
}

function ToolbarNavLink({
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
        active ? 'studio-toolbar-link is-active' : 'studio-toolbar-link'
      }
    >
      {children}
    </Link>
  )
}

export function StudioLayout() {
  const [, setLocation] = useLocation()
  const { projectName } = useParams<{ projectName: string }>()
  const { logout } = useAuth()
  const [project, setProject] = useState<ProjectPayload | null>(null)
  const [loading, setLoading] = useState(Boolean(projectName))

  useEffect(() => {
    if (!projectName) {
      setProject(null)
      setLoading(false)
      return
    }
    setLoading(true)
    let cancelled = false
    ;(async () => {
      try {
        await new Promise((r) => {
          queueMicrotask(r)
        })
        if (cancelled) return
        setProject({ name: projectName })
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [projectName])

  const settingsHref = `/app/projects/${encodeURIComponent(projectName ?? '')}/settings`

  if (!projectName || loading || !project) {
    return (
      <div className="studio-loading-placeholder" role="status" aria-live="polite">
        加载占位
      </div>
    )
  }

  return (
    <ProjectStudioProvider projectName={projectName}>
      <div className="studio-layout">
        <header className="studio-layout-header studio-toolbar">
          <div className="studio-toolbar-row">
            <span className="studio-toolbar-title">{project.name}</span>
            <span className="studio-toolbar-grow" />
            <Link href="~/app/projects" className="studio-toolbar-aux">
              所有项目
            </Link>
            <Link href={`~${settingsHref}`} className="studio-toolbar-aux">
              项目设置
            </Link>
            <button
              type="button"
              className="app-nav-button studio-toolbar-logout"
              onClick={() => {
                logout()
                setLocation('/login')
              }}
            >
              退出
            </button>
          </div>
          <nav className="studio-toolbar-row studio-toolbar-nav" aria-label="工作台">
            <ToolbarNavLink href="/">概览</ToolbarNavLink>
            <ToolbarNavLink href="/characters">角色</ToolbarNavLink>
            <ToolbarNavLink href="/scenes">场次</ToolbarNavLink>
            <ToolbarNavLink href="/props">道具</ToolbarNavLink>
            <ToolbarNavLink href="/lorebook">Lorebook → 角色</ToolbarNavLink>
            <ToolbarNavLink href="/clues">线索 → 场次</ToolbarNavLink>
            <ToolbarNavLink href={`/source/${encodeURIComponent('剧本草稿.md')}`}>
              示例源文件
            </ToolbarNavLink>
            <ToolbarNavLink href="/episodes/1">示例分集 1</ToolbarNavLink>
          </nav>
        </header>
        <StudioCanvasRouter />
      </div>
    </ProjectStudioProvider>
  )
}
