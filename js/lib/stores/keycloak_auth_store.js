import { writable } from 'svelte/store'

function keycloak_auth_store() {
  const { subscribe, set } = writable({ state: 'init', keycloak: {} })
  if (window._config.keycloak !== undefined) {
    import('keycloak-js').then(async ({ default: Keycloak }) => {
      const keycloak = new Keycloak(window._config.keycloak.params)
      const authenticated = await keycloak.init(window._config.keycloak.init)
      keycloak.onTokenExpired = () => {
        console.debug('refreshing expired token...')
        keycloak.updateToken()
          .success(() => {
            set({ state: 'auth', keycloak })
          })
          .error(e => {
            set({ state: 'error', keycloak })
          })
      }
      set({
        state: authenticated ? 'auth' : 'guest',
        keycloak: {
          ...keycloak,
          logout: () => {
            keycloak.logout()
            set({ state: 'guest', keycloak })
          }
        },
      })
    }).catch(err => {
      console.error(err)
      set({ state: 'error', keycloak })
    })
  }
  return { subscribe }
}

const auth = keycloak_auth_store()

export default auth
