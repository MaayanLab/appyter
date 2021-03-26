<script>
  import * as Ansi from '../../Ansi.svelte'
  import collapse from '../../../utils/collapse.js'
  export let data
</script>

<div class="output_text">
  <Ansi data={collapse(data)} />
</div>
