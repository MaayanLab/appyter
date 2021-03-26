<script>
  import output_mimetypes from './output_mimetype'
  import { getContext } from 'svelte'
  import { report_error as report_error_ctx } from '../../lib/appyter_context.js'
  const report_error = getContext(report_error_ctx)

  export let data
  let mimetype
  let missing = []

  $: if (data && data.data) {
    let _missing = []
    for (const _mimetype in data.data) {
      if (!(_mimetype in output_mimetypes)) _missing.push(_mimetype)
      else {
        mimetype = _mimetype
        break
      }
    }
    missing = _missing
  }

  function error() {
    const error_data = {
      type: 'output-mimetype',
      url: window.location.href,
      missing,
    }
    report_error(error_data)
    return JSON.stringify(error_data)
  }
</script>

{#if data.data}
  <div class="output_display_data">
    {#if missing.length > 0}
      <div class="alert" class:alert-danger={!mimetype} class:alert-warning={mimetype}>
        <p>Unhandled output_mimetype renderer, please report this on <a href="https://github.com/MaayanLab/appyter/issues">Appyter Issues</a> with this information:</p>
        <code>{error()}</code>
      </div>
    {/if}
    {#if mimetype}
      <svelte:component this={output_mimetypes[mimetype]} data={data.data[mimetype]} />
    {/if}
  </div>
{/if}
