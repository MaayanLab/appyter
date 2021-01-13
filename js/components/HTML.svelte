<script>
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
        require(['@jupyter-widgets/html-manager/dist/libembed-amd'], (embed) => {
        // require(['@jupyter-widgets/html-manager'], async ({ HTMLManager }) => {
            embed.renderWidgets(el);
            // const manager = new HTMLManager()
            // const model = manager.new_model(JSON.parse(el.innerHTML))
            // await manager.display_view(manager.create_view(model), widgetTag)

            // manager.display_view(el.parentNode)
          }
        )
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
