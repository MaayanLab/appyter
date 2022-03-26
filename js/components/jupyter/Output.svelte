<script>
  import output_types from './output_type'
  import report_error from '@/extras/catalog-integration/report_error'

  export let data

  function error() {
    const error_data = {
      type: 'output-type',
      error: {
        keys: Object.keys(data),
        output_type: data.output_type||null,
        data_keys: Object.keys(data.data||{}),
      },
    }
    report_error(error_data)
    return JSON.stringify(error_data)
  }
</script>

{#if data}
  {#if data.output_type in output_types}
    <svelte:component
      this={output_types[data.output_type]}
      data={data}
    />
  {:else}
    <div class="alert alert-danger">
      <p>Unhandled output_type renderer, please report this on <a href="https://github.com/MaayanLab/appyter/issues">Appyter Issues</a> with this information:</p>
      <code>{error()}</code>
    </div>
  {/if}
{/if}
