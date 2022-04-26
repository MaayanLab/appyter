<script>
  import GridStack from '@/extras/dashboard/GridStack.svelte'
  import Cell from '@/components/jupyter/Cell.svelte'
  import Outputs from '@/components/jupyter/Outputs.svelte'

  import collapse from '@/utils/collapse'

  export let nb
  export let show_code
  export let current_code_cell
</script>

<style>
  :global(html) {
    overflow-x: hidden;
    overflow-y: scroll;
  }
</style>

<GridStack items={nb.cells} let:item={cell}>
  {#if collapse(cell.source) !== ''}
    {#if cell.cell_type === 'code'}
      <Cell type="code" style="border: 1px solid black">
        <Outputs
          index={cell.index}
          data={cell.outputs || []}
        />
      </Cell>
    {/if}
  {/if}
</GridStack>
