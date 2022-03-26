<script>
  import { output_mimetypes, ignored_mimetypes } from './output_mimetype'
  import report_error from '@/extras/catalog-integration/report_error'

  export let data
  let mimetype
  let missing = []

  $: if (data && data.data) {
    let _available = {}
    let _missing = []
    for (const _mimetype in data.data) {
      if (!(_mimetype in output_mimetypes) && !(_mimetype in ignored_mimetypes)) _missing.push(_mimetype)
      else _available[_mimetype] = 1
    }
    for (const _mimetype in output_mimetypes) {
      if (_mimetype in _available) {
        mimetype = _mimetype
        break
      }
    }
    missing = _missing
  }

  function error() {
    const error_data = {
      type: 'output-mimetype',
      error: {
        missing,
        data_keys: Object.keys(data.data),
      },
    }
    report_error(error_data)
    return JSON.stringify(error_data)
  }
</script>

{#if data.data}
  <div class="output_display_data">
    {#if missing.length > 0 && window._config.DEBUG}
      <div class="alert" class:alert-danger={!mimetype} class:alert-warning={mimetype}>
        <p>Unhandled output_mimetype renderer. This message only appears in development, if there is a rendering issue, please report this on <a href="https://github.com/MaayanLab/appyter/issues">Appyter Issues</a> with this information:</p>
        <code>{error()}</code>
      </div>
    {/if}
    {#if mimetype}
      <svelte:component this={output_mimetypes[mimetype]} data={data.data[mimetype]} />
    {/if}
  </div>
{/if}
