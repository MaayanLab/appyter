<script>
  import { onMount } from 'svelte'
  export let data = {}

  onMount(() => {
    window.require(['svelte'], function(svelte) {
      svelte.render(
        document.getElementById(data.args.name),
        data.js_url,
        data,
      )
    })
  })
</script>

<div id={data.args.name} class="loading">
  <script></script>
</div>
