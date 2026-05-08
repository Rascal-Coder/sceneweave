import { Link } from 'wouter'

export function NotFoundPage() {
  return (
    <main className="app-page">
      <h1>404</h1>
      <p className="app-page-lead">未找到页面。</p>
      <p className="not-found-actions">
        <Link href="~/app/projects">返回项目列表</Link>
        {' · '}
        <Link href="/login">登录页</Link>
      </p>
    </main>
  )
}
