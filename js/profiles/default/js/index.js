export function init(window, config) {
  console.debug('Loading...')
  window._config = config
  asyncInit(window)
    .then(function () {
      console.debug('loaded')
    }).catch(function (e) {
      console.error(e)
    })
}

async function asyncInit(window) {
  await Promise.all([
    import('@/lib/svelte_component_mounter')
      .then(({ default: svelte_component_mounter }) => svelte_component_mounter(window)),
    window._config.DEBUG && import('@/lib/livereload')
      .then(({ default: livereload }) => livereload(window))
  ])
}
