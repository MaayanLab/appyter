<script>
  import report_error from '@/extras/catalog-integration/report_error'
  import { tick, getContext } from 'svelte'
  import { script_mimetypes, ignored_mimetypes } from './script_mimetype'

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
    tick().then(async () => {
      const scripts = ref.querySelectorAll('script')
      for (let i = 0; i < scripts.length; i++) {
        const el = scripts[i]
        const type = el.getAttribute('type') || 'application/javascript'
        if (!(type in script_mimetypes)) {
          if (type in ignored_mimetypes) continue
          const error_data = {
            type: 'script-mimetype',
            error: {
              missing: type,
            },
          }
          report_error(error_data)
          continue
        }
        const handler = script_mimetypes[type]
        try {
          await handler(el)
        } catch (e) {
          const error_data = {
            type: 'script-error',
            error: e.toString(),
          }
          report_error(error_data)
        }
      }
    })
  }
</script>

<div bind:this={ref} class={classes}>
  {@html data}
</div>
