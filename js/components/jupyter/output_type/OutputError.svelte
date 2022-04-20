<script>
  import { onMount } from 'svelte'
  import Ansi from '@/components/Ansi.svelte'
  import collapse from '@/utils/collapse.js'
  import report_error from '@/extras/catalog-integration/report_error'

  export let data

  onMount(() => {
    const error_data = {
      type: 'runtime-error',
      error: data,
    }
    report_error(error_data)
  })
</script>

<div class="output_subarea output_test output_error">
  {#if data.traceback !== undefined}
    <Ansi data="{collapse(data.traceback, '\n')}" />
  {:else}
    <Ansi data="{data.ename}: {data.evalue}" />
  {/if}
</div>
