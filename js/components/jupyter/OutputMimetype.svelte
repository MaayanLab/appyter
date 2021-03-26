<script>
  import output_mimetypes from './output_mimetype'

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
    console.error(data)
    return JSON.stringify({
      url: window.location.href,
      missing,
    })
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
