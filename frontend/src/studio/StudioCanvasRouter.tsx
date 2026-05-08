import { useContext } from 'react'
import { Redirect, Route, Switch, useParams } from 'wouter'
import {
  ProjectStudioContext,
  useStudioProject,
} from '@/studio/ProjectStudioContext'

function StudioOverviewCanvas() {
  const { projectName } = useStudioProject()
  return (
    <section className="studio-panel">
      <h2>项目概览画布（占位）</h2>
      <p>StudioOverviewCanvas — {projectName}</p>
    </section>
  )
}

function CharactersPage() {
  const { projectName } = useStudioProject()
  return (
    <section className="studio-panel">
      <h2>角色（占位）</h2>
      <p>Characters — {projectName}</p>
    </section>
  )
}

function ScenesPage() {
  const { projectName } = useStudioProject()
  return (
    <section className="studio-panel">
      <h2>场次（占位）</h2>
      <p>Scenes — {projectName}</p>
    </section>
  )
}

function PropsPage() {
  const { projectName } = useStudioProject()
  return (
    <section className="studio-panel">
      <h2>道具（占位）</h2>
      <p>Props — {projectName}</p>
    </section>
  )
}

function SourceFilePage() {
  const { filename = '' } = useParams<{ filename: string }>()
  const { projectName } = useStudioProject()
  const decoded = filename ? decodeURIComponent(filename) : ''

  return (
    <section className="studio-panel">
      <h2>源文件查看（占位）</h2>
      <p>
        项目：{projectName}；decoded filename：<code>{decoded}</code>
      </p>
    </section>
  )
}

function EpisodeEditorPage() {
  const { episodeId = '' } = useParams<{ episodeId: string }>()
  const { projectName } = useStudioProject()
  const numeric = /^\d+$/.test(episodeId)

  return (
    <section className="studio-panel">
      <h2>分集编辑区（占位）</h2>
      <p>
        项目：{projectName}；episodeId：{episodeId}
        {!numeric ? '（非数字字符串）' : null}
      </p>
    </section>
  )
}

function StudioNestedNotFound() {
  const { projectName } = useStudioProject()
  return (
    <section className="studio-panel">
      <h2>工作台子路由未匹配</h2>
      <p>项目：{projectName}</p>
    </section>
  )
}

export function StudioCanvasRouter() {
  const ctx = useContext(ProjectStudioContext)
  if (!ctx?.projectName) {
    return (
      <div className="studio-loading-placeholder" role="status" aria-live="polite">
        加载占位
      </div>
    )
  }

  return (
    <Switch>
      <Route path="/">
        <StudioOverviewCanvas />
      </Route>
      <Route path="/lorebook">
        <Redirect to="/characters" />
      </Route>
      <Route path="/clues">
        <Redirect to="/scenes" />
      </Route>
      <Route path="/characters">
        <CharactersPage />
      </Route>
      <Route path="/scenes">
        <ScenesPage />
      </Route>
      <Route path="/props">
        <PropsPage />
      </Route>
      <Route path="/source/:filename">
        <SourceFilePage />
      </Route>
      <Route path="/episodes/:episodeId">
        <EpisodeEditorPage />
      </Route>
      <Route>
        <StudioNestedNotFound />
      </Route>
    </Switch>
  )
}
