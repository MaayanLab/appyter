<script>
  /*
   * For compatibility with non-svelte-driven fields, this
   *  lets you use (jinja2 rendered) fields as a svelte component.
   * It does this by rendering the field on the server and inserting
   *  the HTML.
   * TODO: Short-circuit (render component with svelte directly) on
   *  svelte-defined fields: `<svelte:component this={require('component.js')} />`
   **/
  import HTML from '@/components/HTML.svelte'
  import Loader from '@/components/Loader.svelte'
  export let field
  export let args

  let rendered
  async function render() {
    const res = await fetch(`${window._config.ORIGIN}/ssr/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ field, args }),
    })
    try {
      rendered = await res.text()
    } catch (e) {
      rendered = `<div class="alert alert-danger">Error: ${e.toString()}</div>`
    }
  }
  $: if (field !== undefined && args !== undefined) {
    render()
  }
</script>

{#if rendered === undefined}
  <div class="text-center">
    <Loader />
  </div>
{:else}
  <HTML classes="ssr" data={rendered} />
{/if}
