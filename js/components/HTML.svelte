<script>
  import report_error from '@/extras/catalog-integration/report_error'

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

  $: if (ref) ref.querySelectorAll('script').forEach(el => {
    if (el.type === 'application/json') return
    try_eval_once(el.innerHTML)
  })
</script>

<div bind:this={ref} class={classes}>
  {@html data}
</div>
