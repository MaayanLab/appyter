<script>
  import markdown_it from '@/lib/markdown_it'

  export let data
  let rendered

  $: rendered = markdown_it.render(data)
</script>

{@html rendered}
