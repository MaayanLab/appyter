<script>
  import { onMount } from 'svelte'
  import Loader from '@/components/Loader.svelte'
  export let module
  export let props = {}
  export let children = false

  let Component
  onMount(() =>
    module()
      .then(({ default: mod }) => Component = mod)
      .catch((e) => console.error(e))
  )
</script>

{#if Component !== undefined}
  {#if children}
    <Component {...props}>
      <slot></slot>
    </Component>
  {:else}
    <Component {...props} />
  {/if}
{:else}
  <Loader />
{/if}
