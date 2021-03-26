<script>
  import * as Prompt from './Prompt.svelte'
  import output_types from './output_type'

  export let index
  export let data

  function error() {
    console.error(data)
    return JSON.stringify({
      url: window.location.href,
      keys: Object.keys(data),
      output_type: data.output_type||null,
      data_keys: Object.keys(data.data||{}),
    })
  }
</script>

<div class="output_area">
  <Prompt
    index={index}
    prompt_type="output"
  />
  {#if data}
  <div class="output_subarea">
    {#if data.output_type in output_types}
      <svelte:component this={output_types[data.output_type]} data={data} />
    {:else}
      <div class="alert alert-danger">
        <p>Unhandled output_type renderer, please report this on <a href="https://github.com/MaayanLab/appyter/issues">Appyter Issues</a> with this information:</p>
        <code>{error()}</code>
      </div>
    {/if}
  </div>
  {/if}
</div>
