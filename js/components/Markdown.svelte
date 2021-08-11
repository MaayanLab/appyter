<script>
  import { getContext } from 'svelte'
  import { markdown_it as markdown_it_ctx } from '@/lib/appyter_context.js'
  const markdown_it = getContext(markdown_it_ctx)

  export let data
  let rendered

  $: rendered = markdown_it.render(data)
</script>

{@html rendered}
