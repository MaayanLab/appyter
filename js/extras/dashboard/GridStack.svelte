<script>
  import 'gridstack/dist/gridstack.min.css'
  import { onMount } from 'svelte'
  import GridStack from 'gridstack/dist/gridstack-h5'

  export let items = []

  let grid
  onMount(() => {
    grid = GridStack.init()
  })
</script>

<div class="grid-stack">
  {#each items as item}
    <div class="grid-stack-item" gs-w="6" hs-h="4">
      <div class="grid-stack-item-content">
        <slot item={item}></slot>
      </div>
    </div>
  {/each}
</div>
