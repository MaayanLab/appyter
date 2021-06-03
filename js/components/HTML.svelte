<script>
  import { getContext } from 'svelte'
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

  $: if (ref) ref.querySelectorAll('script').forEach(el => try_eval_once(el.innerHTML))
</script>

<div bind:this={ref} class={classes}>
  {@html data}
</div>
