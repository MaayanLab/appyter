import { writable } from 'svelte/store'

function keycloak_auth_store() {
  const initStore = {}
  try {
    Object.assign(initStore, {
      state: 'init',
      keycloak: new Keycloak(window._config.keycloak.params),
    })
  } catch (e) {
    console.error(e)
    Object.assign(initStore, {
      state: 'error',
      keycloak: {},
    })
  }
  const { subscribe, set } = writable(initStore)
  ;(async () => {
    const { keycloak } = initStore
    if ('init' in keycloak) {
      keycloak.init(window._config.keycloak.init)
        .then(authenticated => {
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
  })()
  return { subscribe }
}

const auth = keycloak_auth_store()

export default auth