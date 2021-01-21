<script>
  import get_require from '../utils/get_require'

  export let classes = ""
  export let data = ""
  
  let ref

  let evaled = {}
  function try_eval_once(src) {
    if (evaled[src] === undefined) {
      evaled[src] = true
      try {
        (new Function(src))()
      } catch (e) {
        console.error(e)
      }
    }
  }

  $: if (ref) {
    const scripts = ref.querySelectorAll('script')
    for (let i = 0; i < scripts.length; i++) {
      const el = scripts[i]
      const type = el.getAttribute('type') || 'application/javascript'
      const types = type.split('+')
      if (types.indexOf('json') >= 0) {
        if (type === 'application/vnd.jupyter.widget-view+json') {
          const metadata = JSON.parse(el.innerHTML)
          get_require(window, 'ipywidget-manager').then(async (manager) => {
            if (manager.__models === undefined) {
              manager.__models = {}
            }
            if (manager.__models[metadata.model_id] === undefined) {
              manager.__models[metadata.model_id] = { metadata, el: ref }
            }
          }).catch(console.error)
        } else if (type === 'application/vnd.jupyter.widget-state+json') {
          const metadata = JSON.parse(el.innerHTML)
          get_require(window, 'ipywidget-manager').then(async (manager) => {
            const models = {}
            for (const model of (await manager.set_state(metadata))) {
              models[model.model_id] = model
            }
            if (manager.__models !== undefined) {
              for (const model in manager.__models) {
                if (models[model] !== undefined) {
                  const viewTag = manager.__models[model].el
                  const view = await manager.create_view(models[model])
                  manager.display_view(view, { el: viewTag })
                }
              }
            }
          }).catch(console.error)
        } else {
          console.warn(`Unhandled script type ${type}`)
        }
      } else {
        try_eval_once(el.innerHTML)
      }
    }
  }
</script>

<div bind:this={ref} class={classes}>
  {@html data}
</div>
