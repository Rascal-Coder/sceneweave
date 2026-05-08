import { Link, useParams } from 'wouter'

export function ProjectSettingsPage() {
  const { projectName = '' } = useParams<{ projectName: string }>()
  const studioBase = `/app/projects/${encodeURIComponent(projectName)}`

  return (
    <main className="app-page project-settings-fullscreen">
      <header className="project-settings-bar">
        <Link href="~/app/projects" className="project-settings-back">
          ← 项目列表
        </Link>
        <Link href={`~${studioBase}`} className="project-settings-back">
          进入工作台
        </Link>
      </header>
      <h1>项目设置</h1>
      <p className="app-page-lead">
        项目「{projectName}」— 路径 <code>{studioBase}/settings</code>
      </p>
    </main>
  )
}
