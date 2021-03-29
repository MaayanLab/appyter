<script>
  import { onMount, getContext } from 'svelte'
  import * as Ansi from '../../Ansi.svelte'
  import collapse from '../../../utils/collapse.js'
  import { report_error as report_error_ctx } from '../../../lib/appyter_context.js'
  const report_error = getContext(report_error_ctx)

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
