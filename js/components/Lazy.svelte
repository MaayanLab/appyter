<script>
  import Loader from '@/components/Loader.svelte'
  export let module
  export let props

  let component
  onMount(() => module().then((mod) => component = mod).catch((e) => console.error(e)))
</script>

{#if component !== undefined}
  <svelte:component this={component} {...props}>
    <slot></slot>
  </svelte:component>
{:else}
  <Loader />
{/if}
