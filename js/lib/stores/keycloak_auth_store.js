import { writable } from 'svelte/store'
import hash from '@/lib/stores/url_hash_store.js'

function keycloak_auth_store() {
  const { subscribe, set } = writable({ state: 'init', keycloak: {} })
  if (window._config.EXTRAS.indexOf('catalog-integration') !== -1 && window._config.keycloak !== undefined) {
    import('keycloak-js').then(async ({ default: Keycloak }) => {
      const keycloak = new Keycloak(window._config.keycloak.params)
      const authenticated = await keycloak.init({
        ...window._config.keycloak.init,
        redirectUri: window.location.href + (window.location.href.includes('#') ? '' : '#') + (window.location.href.includes('?') ? '' : '?'),
      })
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
      // cleanup keycloak auth params
      hash.update($hash => {
        const params = { ...$hash.params }
        if ('code' in params) delete params['code']
        if ('session_state' in params) delete params['session_state']
        if ('state' in params) delete params['state']
        return { ...$hash, params }
      })
    }).catch(err => {
      console.error(err)
      set({ state: 'error', keycloak })
    })
  }
  return { subscribe }
}
const auth = keycloak_auth_store()

auth.subscribe(auth => {
  if (auth.state === 'auth' && document.cookie.match(/^(.*;)?\s*authorization\s*=\s*[^;]+(.*)?$/) === null) {
    document.cookie = `authorization=${auth.keycloak.token}; expires=${(new Date(auth.keycloak.tokenParsed.exp*1000)).toUTCString()}; secure`
  }
})

export default auth
