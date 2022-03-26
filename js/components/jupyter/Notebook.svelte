<script>
  import Lazy from '@/components/Lazy.svelte'

  import Cell from '@/components/jupyter/Cell.svelte'
  import Input from '@/components/jupyter/Input.svelte'
  import Prompt from '@/components/jupyter/Prompt.svelte'
  import Source from '@/components/jupyter/Source.svelte'
  import Outputs from '@/components/jupyter/Outputs.svelte'

  import collapse from '@/utils/collapse'
  import any from '@/utils/any'

  export let nb
  export let show_code
  export let current_code_cell
</script>

<Lazy
  module={() => import('@/components/jupyter/Cells.svelte')}
  children
>
  {#each nb.cells as cell (cell.index)}
    {#if collapse(cell.source) !== ''}
      {#if cell.cell_type === 'code'}
        <Cell type="code">
          {#if show_code}
            <Input>
              <Prompt
                prompt_type="input"
                index={cell.index}
                running={current_code_cell !== undefined ? cell.index >= current_code_cell : undefined}
                error={any(cell.outputs.map(({ output_type }) => output_type === 'error'))}
                counter={cell.execution_count}
                cell_type={cell.cell_type}
              />
              <Source
                language="python"
                source={collapse(cell.source)}
              />
            </Input>
          {/if}
          <Outputs
            index={cell.index}
            data={cell.outputs || []}
            loading={current_code_cell}
          />
        </Cell>
      {:else if cell.cell_type === 'markdown'}
        <Cell type="text">
          <Input>
            <Prompt
              prompt_type="input"
              index={cell.index}
            />
            <div class="inner_cell">
              <div class="text_cell_render border-box-sizing rendered_html">
                <Lazy
                  module={() => import('@/components/Markdown.svelte')}
                  props={{data: collapse(cell.source)}}
                />
              </div>
            </div>
          </Input>
        </Cell>
      {/if}
    {/if}
  {/each}
</Lazy>
