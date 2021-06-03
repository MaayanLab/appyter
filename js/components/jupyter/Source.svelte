<script>
  import Markdown from '@/components/Markdown.svelte'

  export let language
  export let source
</script>

<div class="inner_cell">
  <div class="input_area">
    <div class="highlight hl-ipython3">
      <Markdown data={'\n```' + language + '\n' + source + '\n```\n'} />
    </div>
  </div>
</div>
