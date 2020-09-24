<script>
  export let classes = ""
  export let data = ""
  
  let ref

  let evaled = {}
  function try_eval_once(src) {
    if (evaled[src] === undefined) {
      evaled[src] = true
      try {
        (new Function(src))()
      } catch (e) {
        console.error(e)
      }
    }
  }

  $: {
    if (ref) ref.querySelectorAll('script').forEach(el => try_eval_once(el.innerHTML))
    console.log('HTML')
    console.log(data)
  }
</script>

<div bind:this={ref} class={classes}>
  {@html data}
</div>
