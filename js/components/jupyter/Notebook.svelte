<script>
  import Lazy from '@/components/Lazy.svelte'
  import HTML from '@/components/HTML.svelte'

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

  function isMainHeading(cell) {
    return (
      cell.cell_type === 'markdown' &&
      collapse(cell.source).trim().startsWith('# ')
    )
  }
</script>

<Lazy
  module={() => import('@/components/jupyter/Cells.svelte')}
  children
>
  {#let inCard = false}

  {#each nb.cells as cell (cell.index)}

    {#if collapse(cell.source) === ''}
    {:else}

      {#if isMainHeading(cell)}
        {#if inCard}
          </div> 
        {/if}

        <!-- open new card -->
        <div class="section-card">
          {#let inCard = true}

          <div class="section-header">
            <Lazy
              module={() => import('@/components/Markdown.svelte')}
              props={{ data: collapse(cell.source) }}
            />
          </div>
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
  {#if window._config.EXTRAS.indexOf('ipywidgets') !== -1 && nb.metadata.widgets !== undefined && nb.metadata.widgets['application/vnd.jupyter.widget-state+json'] !== undefined}
    <HTML data="<script type='application/vnd.jupyter.widget-state+json'>{JSON.stringify(nb.metadata.widgets['application/vnd.jupyter.widget-state+json'])}</script>" />
  {/if}
</Lazy>

<style>
  .section-card {
    margin: 2rem 0;
    padding: 1.5rem;
    border-radius: 14px;
    background: white;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  }

  .section-header {
    margin-bottom: 1rem;
    border-bottom: 1px solid #eee;
  }
</style>