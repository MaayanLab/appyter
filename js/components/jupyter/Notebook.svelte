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

  function isHeading(source) {
    const collapsed = collapse(source).trim()
    const isH1 = collapsed.startsWith('# ') && !collapsed.startsWith('## ')
    return isH1
  }

  // Pre-process cells to group them into sections
  function groupCellsIntoSections(cells) {
    const sections = []
    let currentSection = { cells: [], hasHeading: false, collapsed: false }
    
    cells.forEach((cell, idx) => {
      if (collapse(cell.source) === '') return
      
      if (cell.cell_type === 'markdown' && isHeading(cell.source)) {
        // Start a new section
        if (currentSection.cells.length > 0) {
          sections.push(currentSection)
        }
        currentSection = { cells: [cell], hasHeading: true, collapsed: false }
      } else {
        currentSection.cells.push(cell)
      }
    })
    
    // Add the last section
    if (currentSection.cells.length > 0) {
      sections.push(currentSection)
    }
    
    return sections
  }

  $: sections = groupCellsIntoSections(nb.cells)

  function toggleSection(sectionIdx) {
    sections[sectionIdx].collapsed = !sections[sectionIdx].collapsed
    sections = [...sections] // Create new array to trigger reactivity
  }

  function handleKeyPress(event, sectionIdx) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      toggleSection(sectionIdx)
    }
  }
</script>

<Lazy
  module={() => import('@/components/jupyter/Cells.svelte')}
  children
>
  {#each sections as section, sectionIdx}
    <div class="section-card" class:has-heading={section.hasHeading}>
      {#each section.cells as cell, cellIdx (cell.index)}
        {#if cellIdx === 0 || !section.collapsed}
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
                    {#if section.hasHeading && cellIdx === 0}
                      <div 
                        class="heading-wrapper" 
                        role="button"
                        tabindex="0"
                        on:click={() => toggleSection(sectionIdx)}
                        on:keypress={(e) => handleKeyPress(e, sectionIdx)}
                      >
                        <span class="collapse-icon">{section.collapsed ? '▶' : '▼'}</span>
                        <Lazy
                          module={() => import('@/components/Markdown.svelte')}
                          props={{data: collapse(cell.source)}}
                        />
                      </div>
                    {:else}
                      <Lazy
                        module={() => import('@/components/Markdown.svelte')}
                        props={{data: collapse(cell.source).replace("H#", "#")}}
                      />
                    {/if}
                  </div>
                </div>
              </Input>
            </Cell>
          {/if}
        {/if}
      {/each}
    </div>
  {/each}
  {#if window._config.EXTRAS.indexOf('ipywidgets') !== -1 && nb.metadata.widgets !== undefined && nb.metadata.widgets['application/vnd.jupyter.widget-state+json'] !== undefined}
    <HTML data="<script type='application/vnd.jupyter.widget-state+json'>{JSON.stringify(nb.metadata.widgets['application/vnd.jupyter.widget-state+json'])}</script>" />
  {/if}
</Lazy>

<style>
  .section-card {
    margin-bottom: 1.5rem;
    padding: 1.5rem;
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .heading-wrapper {
    cursor: pointer;
    display: flex;
    align-items: flex-start;
    user-select: none;
  }

  .heading-wrapper:hover {
    opacity: 0.8;
  }

  .heading-wrapper:focus {
    outline: 2px solid #4CAF50;
    outline-offset: 2px;
  }

  .collapse-icon {
    margin-right: 0.5rem;
    font-size: 0.8em;
    min-width: 1em;
    display: inline-block;
  }

  /* Optional: remove card styling for pre-heading content */
  .section-card:not(.has-heading) {
    border: none;
    box-shadow: none;
    background-color: transparent;
    padding: 0;
  }
</style>