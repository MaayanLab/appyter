<script>
  export let counter
  export let running
</script>

<div class="prompt input_prompt">
  {#if counter || running}
    In&nbsp;[{#if running}*{:else if counter}{counter}{:else}&nbsp;{/if}]
  {/if}
</div>
