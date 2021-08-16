<script>
  import Ansi from '@/components/Ansi.svelte'
  import collapse from '@/utils/collapse.js'
  export let data
</script>

<div class="output_stream output_{data.name} output_text">
  <Ansi data={collapse(data.text)} />
</div>
