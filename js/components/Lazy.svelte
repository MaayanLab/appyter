<script>
  import { onMount } from 'svelte'
  import Loader from '@/components/Loader.svelte'
  export let module
  export let props = {}
  export let children = false

  let component
  onMount(() =>
    module()
      .then(({ default: mod }) => component = mod)
      .catch((e) => console.error(e))
  )
</script>

{#if component !== undefined}
  {#if children}
    <svelte:component this={component} {...props}>
      <slot></slot>
    </svelte:component>
  {:else}
    <svelte:component this={component} {...props} />
  {/if}
{:else}
  <Loader />
{/if}
