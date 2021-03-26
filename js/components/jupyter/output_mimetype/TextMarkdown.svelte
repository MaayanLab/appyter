<script>
  import * as Markdown from '../../Markdown.svelte'
  import collapse from '../../../utils/collapse.js'
  export let data
</script>

<div class="output_markdown">
  <Markdown data={collapse(data)} />
</div>
