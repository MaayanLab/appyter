<script>
  export let cell_type
  export let counter
  export let running
  export let error
</script>

<div class="prompt input_prompt">
  {#if cell_type === 'code'}
    {#if error}
      <b style="color: red">In&nbsp;[E]:</b>
    {:else}
      In&nbsp;[{#if running}*{:else if counter}{counter}{:else}&nbsp;{/if}]
    {/if}
  {/if}
</div>
