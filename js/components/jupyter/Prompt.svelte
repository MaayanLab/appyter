<script>
  export let index
  export let prompt_type
  export let cell_type = undefined
  export let counter = undefined
  export let running = undefined
  export let error = undefined
</script>

<div id="{prompt_type}-prompt-{index}" class="prompt {prompt_type}_prompt">
  {#if cell_type === 'code'}
    {#if running}
      In&nbsp;[*]
    {:else if error}
      <b style="color: red">In&nbsp;[E]:</b>
    {:else if counter}
      In&nbsp;[{counter}]
    {:else}
      In&nbsp;[ ]
    {/if}
  {/if}
  <a class="prompt-anchor" href="#{prompt_type}-prompt-{index}">¶</a>
</div>
