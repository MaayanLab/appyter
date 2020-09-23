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

  $: if (ref) ref.querySelectorAll('script').forEach(el => try_eval_once(el.innerHTML))
</script>

<div this:ref={ref} class={classes}>
  {@html data}
</div>
