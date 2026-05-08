import { Route, Switch, Redirect } from 'wouter'
import { AppShell } from '@/components/AppShell'
import { AuthGuard } from '@/routes/AuthGuard'
import { LoginPage } from '@/pages/LoginPage'
import { ProjectsPage } from '@/pages/ProjectsPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { AssetsPage } from '@/pages/AssetsPage'
import { ProjectSettingsPage } from '@/pages/ProjectSettingsPage'
import { NotFoundPage } from '@/pages/NotFoundPage'
import { StudioLayout } from '@/studio/StudioLayout'

export function AppRoutes() {
  return (
    <Switch>
      <Route path="/login" component={LoginPage} />

      <Route path="/">
        <Redirect to="/app/projects" />
      </Route>

      <Route path="/app/projects/:projectName/settings">
        <AuthGuard>
          <ProjectSettingsPage />
        </AuthGuard>
      </Route>

      <Route path="/app/projects/:projectName" nest>
        <AuthGuard>
          <StudioLayout />
        </AuthGuard>
      </Route>

      <Route path="/app/projects">
        <AuthGuard>
          <AppShell>
            <ProjectsPage />
          </AppShell>
        </AuthGuard>
      </Route>

      <Route path="/app/settings">
        <AuthGuard>
          <AppShell>
            <SettingsPage />
          </AppShell>
        </AuthGuard>
      </Route>

      <Route path="/app/assets">
        <AuthGuard>
          <AppShell>
            <AssetsPage />
          </AppShell>
        </AuthGuard>
      </Route>

      <Route path="/app">
        <AuthGuard>
          <Redirect to="/app/projects" />
        </AuthGuard>
      </Route>

      <Route>
        <NotFoundPage />
      </Route>
    </Switch>
  )
}
