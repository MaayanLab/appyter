<script>
  import Markdown from '@/components/Markdown.svelte'
  import collapse from '@/utils/collapse.js'
  export let data
</script>

<div class="output_markdown">
  <Markdown data={collapse(data)} />
</div>
