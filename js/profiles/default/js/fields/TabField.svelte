<script>
  import TabField from '@/components/fields/TabField.svelte'
  import SSRField from '@/components/app/SSRField.svelte'
  export let args
</script>

<TabField bind:args={args} let:tab={tab}>
  {#if tab !== undefined && tab !== null}
    {#each Object.values(args.choices[tab]) as field}
      <SSRField
        field={field.field}
        args={field.args}
      />
    {/each}
  {/if}
</TabField>

<input
  type="text"
  class="hidden"
  name={args.name}
  value={args.value}
/>
