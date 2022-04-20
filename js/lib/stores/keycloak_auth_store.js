import { writable } from 'svelte/store'
import hash from '@/lib/stores/url_hash_store.js'
import with_timeout from '@/utils/with_timeout'

function keycloak_auth_store() {
  const enabled = window._config.EXTRAS.includes('catalog-integration') && window._config.keycloak !== undefined
  const { subscribe, set } = writable({
    state: enabled ? 'init' : 'error',
    keycloak: {},
  })
  if (enabled) {
    import('keycloak-js').then(with_timeout(async ({ default: Keycloak }) => {
      const keycloak = new Keycloak(window._config.keycloak.params)
      const keycloakLogout = keycloak.logout
      Object.assign(keycloak, {
        getValidToken: async () => {
          try {
            await keycloak.updateToken(30)
          } catch (e) {
            console.error(e)
            set({ state: 'guest', keycloak })
          }
          return keycloak.token
        },
        logout: () => {
          keycloakLogout()
          set({ state: 'guest', keycloak })
        },
      })
      const authenticated = await keycloak.init({
        ...window._config.keycloak.init,
        redirectUri: window.location.href + (window.location.href.includes('#') ? '' : '#') + (window.location.href.includes('?') ? '' : '?'),
      })
      set({
        state: authenticated ? 'auth' : 'guest',
        keycloak,
      })
      // cleanup keycloak auth params
      hash.update($hash => {
        const params = { ...$hash.params }
        if ('code' in params) delete params['code']
        if ('session_state' in params) delete params['session_state']
        if ('state' in params) delete params['state']
        return { ...$hash, params }
      })
    }, 5000)).catch(err => {
      console.error(err)
      set({ state: 'error', keycloak: {} })
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
