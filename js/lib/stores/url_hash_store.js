import { writable } from 'svelte/store'

function params_parse(params_encoded) {
  if (params_encoded === '') return {}
  return params_encoded
    .split('&')
    .map(param_pair => param_pair.split('=').map(decodeURIComponent))
    .reduce((params, [key, value]) => ({ ...params, [key]: value !== undefined ? value : true }), {})
}

function params_stringify(params) {
  return Object.keys(params)
    .filter(param => params[param] !== undefined && params[param] !== '')
    .map((param) => params[param] === true ? encodeURIComponent(param) : [param, params[param]].map(encodeURIComponent).join('='))
    .join('&')
}

function fragment_parse(hash_encoded) {
  // if (!hash_encoded.startsWith('/')) hash_encoded = `/${hash_encoded}`
  const q = hash_encoded.indexOf('?')
  if (q === -1) {
    return { path: hash_encoded, params: {} }
  } else {
    const [path, params_encoded] = [hash_encoded.slice(0, q), hash_encoded.slice(q + 1)]
    const params = params_parse(params_encoded)
    return { path, params }
  }
}

function hash_stringify({ path, params }) {
  const params_encoded = params_stringify(params)
  if (params_encoded === '') {
    return path
  } else {
    return `${path}?${params_encoded}`
  }
}

function fragment_get() {
  return (window.location.hash || '#').slice(1)
}

function server_get() {
  return `${window.location.pathname}${window.location.search}`
}

function url_hash_store() {
  const { path: initPath, params: initParams, server: initServer } = { ...fragment_parse(fragment_get()), server: fragment_parse(server_get()) }
  const { subscribe, update, set } = writable({ path: initPath, params: initParams, server: initServer })
  let lastPath = initPath
  subscribe(({ path, params, server }) => {
    const newHash = hash_stringify({ path, params })
    if (path !== lastPath) {
      // add changes to path to history
      window.location.hash = newHash
      lastPath = path
    } else {
      // don't add changes to params to history, but modify the hash url
      const url = `${window.location.origin}${window.location.pathname}${window.location.search}`
      history.replaceState(undefined, undefined, newHash !== '' ? `${url}#${newHash}` : url)
    }
  })
  window.addEventListener('hashchange', () => set({ ...fragment_parse(fragment_get()), initServer }))

  return {
    subscribe,
    update,
    set,
  }
}

const hash = url_hash_store()
export default hash