import { Link } from 'wouter'
import { DEMO_PROJECT_SLUGS } from '@/constants/demoProjects'

export function ProjectsPage() {
  return (
    <main className="app-page">
      <h1>项目</h1>
      <p className="app-page-lead">
        选择项目进入工作台，或打开项目设置（全屏）。
      </p>
      <ul className="project-link-list">
        {DEMO_PROJECT_SLUGS.map((slug) => {
          const hrefBase = `/app/projects/${encodeURIComponent(slug)}`
          return (
            <li key={slug}>
              <Link href={hrefBase} className="project-link-main">
                {slug}
              </Link>
              <span className="project-link-meta">
                <Link href={`${hrefBase}/settings`} className="project-link-secondary">
                  项目设置
                </Link>
              </span>
            </li>
          )
        })}
      </ul>
    </main>
  )
}
