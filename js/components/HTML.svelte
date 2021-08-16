<script>
  import { getContext } from 'svelte'
  import get_require from '@/utils/get_require'
  import { report_error as report_error_ctx } from '@/lib/appyter_context.js'
  const report_error = getContext(report_error_ctx)

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
        const error_data = {
          type: 'javascript-cell',
          error: e.toString(),
        }
        report_error(error_data)
      }
    }
  }

  $: if (ref && data) {
    const scripts = ref.querySelectorAll('script')
    for (let i = 0; i < scripts.length; i++) {
      const el = scripts[i]
      const type = el.getAttribute('type') || 'application/javascript'
      const types = type.split('+')
      if (types.indexOf('json') >= 0) {
        if (type === 'application/vnd.jupyter.widget-view+json') {
          const metadata = JSON.parse(el.innerHTML)
          get_require(window, 'ipywidget-manager').then(async (manager) => {
            await manager.register_view({ metadata, el: ref })
          }).catch(console.error)
        } else if (type === 'application/vnd.jupyter.widget-state+json') {
          const metadata = JSON.parse(el.innerHTML)
          get_require(window, 'ipywidget-manager').then(async (manager) => {
            await manager.register_state(metadata)
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
