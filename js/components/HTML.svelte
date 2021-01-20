<script>
  import { IPYWidgetManager } from '../lib/ipywidget'

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
      if (type === 'application/vnd.jupyter.widget-view+json') {
        const manager = new IPYWidgetManager()
        const model = JSON.parse(el.innerHTML)
        manager.new_model(model)
          .then((model) => {
            console.log('create view')
            // get state
            return model.create_view(model)
          })
          .then((view) => {
            console.log('display view')
            manager.display_view(null, view)
            return view
          })
          .catch(console.error)
        continue
      }
      const types = type.split('+')
      if (types.indexOf('json') >= 0) {
        continue
      }
      try_eval_once(el.innerHTML)
    }
  }
</script>

<div bind:this={ref} class={classes}>
  {@html data}
</div>
