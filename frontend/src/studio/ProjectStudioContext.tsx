import {
  createContext,
  useContext,
  type ReactNode,
} from 'react'

type ProjectStudioValue = {
  projectName: string
}

export const ProjectStudioContext = createContext<ProjectStudioValue | null>(
  null,
)

export function ProjectStudioProvider({
  projectName,
  children,
}: {
  projectName: string
  children: ReactNode
}) {
  return (
    <ProjectStudioContext.Provider value={{ projectName }}>
      {children}
    </ProjectStudioContext.Provider>
  )
}

/** 工作台嵌套路由内需 projectName 时使用（子路由 useParams 不含父级动态段）。 */
export function useStudioProject(): ProjectStudioValue {
  const ctx = useContext(ProjectStudioContext)
  if (!ctx) {
    throw new Error('useStudioProject 须在 ProjectStudioProvider 内使用')
  }
  return ctx
}
