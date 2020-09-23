<script>
  import { tick, onMount } from 'svelte'
  import * as Cells from '../../../../components/jupyter/Cells.svelte'
  import * as Cell from '../../../../components/jupyter/Cell.svelte'
  import * as Input from '../../../../components/jupyter/Input.svelte'
  import * as Prompt from '../../../../components/jupyter/Prompt.svelte'
  import * as Source from '../../../../components/jupyter/Source.svelte'
  import * as Outputs from '../../../../components/jupyter/Outputs.svelte'
  import * as Markdown from '../../../../components/jupyter/Markdown.svelte'
  import collapse from '../../../../utils/collapse'
  import slugify from '../../../../utils/slugify'
  import any from '../../../../utils/any'
  import hash from '../../../../utils/hash'

  export let window
  export let nbdownload
  export let extras = []

  let nb
  let show_code = false

  // get deps with requirejs
  let socket
  let _deps = undefined
  async function ensure_deps() {
    if (_deps === undefined) {
      _deps = await new Promise(
        (resolve, reject) =>
          window.require(['socket'], function (socket, SocketIOFileUpload) {
            resolve({ socket })
          }, reject)
      )
      socket = _deps.socket
    }
  }
  async function ensure_connected() {
    if (!socket.connected) {
      await new Promise((resolve, reject) => socket.on('connect', resolve))
    }
  }

  // table of contents
  function *get_md_headers(md) {
    let re = /^(#+)(\s|(<[^>]+>))*(.+?)(\s|(<[^>]+>))*$/gm
    let m
    while ((m = re.exec(md)) !== null) {
      yield { h: m[1].length, label: m[2] }
    }
  }

  let toc
  $: {
    if (nb !== undefined && nb.cells !== undefined && extras.indexOf('toc') !== -1) {
      toc = nb.cells
        .filter(({ cell_type }) => cell_type === 'markdown')
        .reduce((headers, { source }) => [
          ...headers,
          ...get_md_headers(collapse(source, '\n'))
        ], [])
    }
  }

  // dynamic notebook
  let status
  let statusBg = 'primary'
  var current_code_cell

  async function setup_async_exec() {
    socket.on('status', async (value) => {
      await tick()
      status = value
      statusBg = 'primary'
      if (status === 'Success') {
        current_code_cell = undefined
      }
    })
    socket.on('error', async (value) => {
      await tick()
      current_code_cell = undefined
      status = `Error: ${value}`
      statusBg = 'danger'
    })
    socket.on('nb', async (value) => {
      await tick()
      nb = {...value, cells: value.cells.map((cell, index) => ({ ...cell, index })) }
    })
    socket.on('progress', async (value) => {
      await tick()
      current_code_cell = value
    })
    socket.on('cell', async (value_index) => {
      let value = value_index[0]
      let cell_index = value_index[1]
      await tick()
      nb.cells[cell_index] = {...nb.cells[cell_index], ...value}
    })
  }

  async function execute() {
    await ensure_deps()
    await ensure_connected()
    await setup_async_exec()
    const paths = window.location.pathname.split('/').filter(p => p)
    socket.emit('submit', paths[paths.length - 1])
  }

  // initialization
  onMount(async () => {
    await tick()
    status = 'Loading...'
    show_code = extras.indexOf('hide-code') === -1

    try {
      // Load notebook
      const req = await fetch(nbdownload)
      const value = await req.json()
      await tick()
      nb = {...value, cells: value.cells.map((cell, index) => ({ ...cell, index })) }

      if (nb.metadata.execution_info === undefined) {
        // Execute notebook if it hasn't already been executed
        await execute()
      } else {
        status = undefined
      }
    } catch (e) {
      status = `Error: ${e}`
      statusBg = 'danger'
    }
  })
</script>

{#if toc !== undefined}
  <style>
    .toc {
      display: block;
    }
    .toc.h1 {
      font-size: 150%;
      text-indent: 0em;
    }
    .toc.h2 {
      font-size: 140%;
      text-indent: 1em;
    }
    .toc.h3 {
      font-size: 130%;
      text-indent: 1.5em;
    }
    .toc.h4 {
      font-size: 120%;
      text-indent: 1.75em;
    }
    .toc.h5 {
      font-size: 110%;
      text-indent: 1.85em;
    }
    .toc.h6 {
      font-size: 100%;
      text-indent: 2em;
    }
  </style>
{/if}

<style>
  /* markdown-it-anchors */
  :global(a.header-anchor) {
    text-decoration: none;
    cursor: pointer;
  }
  :global(h1) {
    display: block;
  }
  :global(h1) :global(.header-anchor) { 
    display: none;
  }
  :global(h1):hover :global(.header-anchor) { 
    display: inline-block;
  }
  :global(h2) {
    display: block;
  }
  :global(h2) :global(.header-anchor) {
    display: none;
  }
  :global(h2):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h3) {
    display: block;
  }
  :global(h3) :global(.header-anchor) {
    display: none;
  }
  :global(h3):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h4) {
    display: block;
  }
  :global(h4) :global(.header-anchor) {
    display: none;
  }
  :global(h4):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h5) {
    display: block;
  }
  :global(h5) :global(.header-anchor) {
    display: none;
  }
  :global(h5):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h6) {
    display: block;
  }
  :global(h6) :global(.header-anchor) {
    display: none;
  }
  :global(h6):hover :global(.header-anchor) {
    display: inline-block;
  }
</style>

<div class="row">
  <div class="col-sm-12 text-center">
    <a
      id="download-notebook"
      class="btn btn-primary"
      role="button"
      href="{nbdownload}"
    >Download Notebook</a>
    {#if extras.indexOf('toggle-code') !== -1}
      <a
        href="javascript:"
        class="btn btn-secondary white"
        on:click={() => show_code = !show_code}
      >
        Toggle Code
      </a>
    {/if}
  </div>
  <div class="w-100">&nbsp;</div>
  {#if status}
    <div class="col-sm-8 offset-sm-2">
      <div class="alert alert-{statusBg}" role="alert">
        {status}
      </div>
    </div>
  {/if}
  <div class="w-100"></div>
  {#if toc !== undefined}
    <div class="col-sm-12 col-md-3 col-xl-2">
      <div class="row sticky-top">
        <div class="offset-sm-2 col-sm-8 col-md-12">
          <div class="mt-5">
            <legend>Table Of Contents</legend>
            {#each toc as {h, label}}
              <a
                href="#{slugify(label)}"
                class="toc h{h}"
              >
                <Markdown data={label} />
              </a>
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/if}
  <div
    class="col-sm-12"
    class:col-md-9={toc !== undefined}
    class:col-xl-10={toc !== undefined}
  >
    {#if nb}
      <Cells>
        {#each nb.cells as cell (hash(cell))}
          {#if collapse(cell.source) !== ''}
            {#if cell.cell_type === 'code'}
              <Cell type="code">
                {#if show_code}
                  <Input>
                    <Prompt
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
                <Outputs data={cell.outputs || []} />
              </Cell>
            {:else if cell.cell_type === 'markdown'}
              <Cell type="text">
                <Input>
                  <Prompt />
                  <div class="inner_cell">
                    <div class="text_cell_render border-box-sizing rendered_html">
                      <Markdown data={collapse(cell.source)} />
                    </div>
                  </div>
                </Input>
              </Cell>
            {/if}
          {/if}
        {/each}
      </Cells>
    {/if}
  </div>
</div>
