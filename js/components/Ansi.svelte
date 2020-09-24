<script>
  import AnsiUp from 'ansi_up'

  export let data
  let rendered

  const ansi_up = new AnsiUp

  $: rendered = ansi_up.ansi_to_html(data)
</script>

<pre>{@html rendered}</pre>
