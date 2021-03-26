<script>
  import * as Ansi from '../../Ansi.svelte'
  import collapse from '../../../utils/collapse.js'
  export let data
</script>

<div class="output_subarea output_test output_error">
  {#if data.traceback !== undefined}
    <Ansi data="{collapse(data.traceback, '\n')}" />
  {:else}
    <Ansi data="{data.ename}: {data.evalue}" />
  {/if}
</div>
