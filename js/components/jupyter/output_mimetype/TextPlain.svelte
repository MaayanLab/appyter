<script>
  import Ansi from '@/components/Ansi.svelte'
  import collapse from '@/utils/collapse.js'
  export let data
  let _data
  $: _data = collapse(data)
</script>

{#if _data && _data !== '""' && _data !== "''"}
<div class="output_text">
  <Ansi data={_data} />
</div>
{/if}
