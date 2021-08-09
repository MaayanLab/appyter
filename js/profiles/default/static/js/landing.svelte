<script>
  import { tick, onMount, setContext } from 'svelte'
  import Cells from '@/components/jupyter/Cells.svelte'
  import Cell from '@/components/jupyter/Cell.svelte'
  import Input from '@/components/jupyter/Input.svelte'
  import Prompt from '@/components/jupyter/Prompt.svelte'
  import Source from '@/components/jupyter/Source.svelte'
  import Outputs from '@/components/jupyter/Outputs.svelte'
  import Markdown from '@/components/Markdown.svelte'
  import Loader from '@/components/Loader.svelte'
  import collapse from '@/utils/collapse'
  import any from '@/utils/any'
  import get_require from '@/utils/get_require'
  import { setup_chunking } from '@/lib/socketio'
  import { report_error as report_error_ctx, debug as debug_ctx } from '@/lib/appyter_context'

  export let window
  export let nbdownload
  export let extras = []
  export let debug = false

  const paths = window.location.pathname.split('/').filter(p => p)
  const session_id = paths[paths.length - 1]

  let nb
  let notebookRef
  let show_code = false
  let local_run_url

  setContext(debug_ctx, debug)

  setContext(report_error_ctx, async ({ type, error }) => {
    console.error(`[${type}]`, error)
    if (extras.indexOf('catalog-integration') !== -1) {
      try {
        const report_error = await get_require(window, 'report_error')
        report_error({
          appyter: ((nb || {}).metadata || {}).appyter || null,
          url: window.location.href,
          type,
          error,
        })
      } catch (e) {
        console.error('catalog-integration: failed to locate report_error handler')
      }
    }
  })

  // table of contents
  let toc
  onMount(() => {
    if (extras.indexOf('toc') !== -1 && notebookRef !== undefined) {
      const observer = new MutationObserver(mutations => {
        // look through mutations and update update toc iff a header element was added/removed
        for (const mutation of mutations) {
          if (mutation.type !== 'childList') continue
          for (const e of [...mutation.addedNodes, ...mutation.removedNodes]) {
            if (e.tagName !== undefined && e.tagName.startsWith('H')) {
              toc = [...notebookRef.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e => ({
                h: e.tagName.slice(1),
                textContent: e.textContent.replace(/ ¶$/, ''),
                id: e.id,
              })).filter(({ id }) => id)
              return
            }
          }
        }
      })
      observer.observe(notebookRef, { childList: true, subtree: true })
    }
  })

  // dynamic notebook
  let status
  let statusBg = 'primary'
  var current_code_cell

  async function setup_async_exec(socket) {
    socket.on('connect', async () => {
      await tick()
      status = `Connected to server, re-initializing...`
      statusBg = 'warning'
      await init()
    })
    socket.on('reconnect', async () => {
      await tick()
      status = `Reconnecting to server...`
      statusBg = 'warning'
    })
    socket.on('disconnect', async (reason) => {
      if (reason !== 'io client disconnect') {
        await tick()
        status = `Disconnected from server...`
        statusBg = 'danger'
      }
    })
    socket.on('status', async (value) => {
      await tick()
      status = value
      statusBg = 'primary'
      if (status === 'Success') {
        current_code_cell = undefined
        if (!debug) {
          socket.disconnect()
        }
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
    setup_chunking(socket)
  }

  let connect_init = false
  async function connect(execute) {
    const socket = await get_require(window, 'socket')
    if (!connect_init) {
      connect_init = true
      // ensure we're connected
      await new Promise((resolve, reject) => {
        if (socket.connected) resolve()
        else socket.on('connect', resolve)
      })
      await setup_async_exec(socket)
    }
    if (execute) {
      socket.emit('submit', session_id)
    } else {
      socket.emit('join', session_id)
    }
  }

  async function init() {
    let pagehit_type = 'view'
    try {
      // Load notebook
      // https://developer.mozilla.org/en-US/docs/Web/API/Request/cache
      // no-cache implies a check with the remote server no matter what, it still uses the cache if the resource hasn't changed
      const req = await fetch(nbdownload, {cache: 'no-cache'})
      if (req.status === 404) {
        throw new Error('Notebook not found')
      }
      const value = await req.json()
      if (value.metadata.appyter === undefined) {
        console.warn('Converting legacy metadata')
        value.metadata.appyter = {
          nbconstruct: {},
        }
        if (value.metadata.execution_info !== undefined) {
          value.metadata.appyter.nbexecute = {
            started: value.metadata.execution_info.started,
            completed: value.metadata.execution_info.completed,
          }
        }
      }
      if (nb === undefined) {
        nb = {...value, cells: value.cells.map((cell, index) => ({ ...cell, index })) }
      }

      if (value.metadata.appyter.nbexecute === undefined) {
        // Execute notebook if it hasn't already been executed
        await connect(true)
        pagehit_type = 'execute'
      } else {
        if (value.metadata.appyter.nbexecute.completed === undefined) {
          // Notebook started but hasn't completed
          await connect(false)
          await tick()
          status = 'Notebook is currently executing, joining session...'
          statusBg = 'primary'
        } else {
          await tick()
          status = undefined
          nb = {...value, cells: value.cells.map((cell, index) => ({ ...cell, index })) }
        }
      }
    } catch (e) {
      await tick()
      status = `${e}`
      statusBg = 'danger'
    }

    if (extras.indexOf('catalog-integration') !== -1) {
      // setup local run appyter link
      try {
        const slug = paths[paths.length - 2] || ''

        let appyter_version = ''
        if (nb.metadata.appyter.info !== undefined) appyter_version = nb.metadata.appyter.info.version || ''

        let library_version = ''
        if (nb.metadata.appyter.nbexecute !== undefined) library_version = nb.metadata.appyter.nbexecute.version || ''
        else if (nb.metadata.appyter.nbconstruct !== undefined) library_version = nb.metadata.appyter.nbconstruct.version || ''

        local_run_url = `${window.location.origin}/#/running-appyters/?slug=${slug}&appyter_version=${appyter_version}&library_version=${library_version}&id=${session_id}`
      } catch (e) {
        console.error('catalog-integration: local_run_url setup error')
        console.error(e)
      }

      // trigger pagehit
      try {
        const pagehit = await get_require(window, 'pagehit')
        pagehit(pagehit_type)
      } catch (e) {
        console.error('catalog-integration: pagehit error')
        console.error(e)
      }
    }
  }

  // initialization
  onMount(async () => {
    await tick()
    status = 'Loading...'
    statusBg = 'primary'
    show_code = extras.indexOf('hide-code') === -1
    await init()
  })
</script>

{#if toc !== undefined}
  <style>
    .toc {
      display: block;
      font-weight: bold;
    }
    .toc.h1 {
      font-size: 100%;
      text-indent: 0em;
    }
    .toc.h2 {
      font-size: 90%;
      text-indent: 1em;
    }
    .toc.h3 {
      font-size: 80%;
      text-indent: 1.5em;
    }
    .toc.h4 {
      font-size: 70%;
      text-indent: 1.75em;
    }
    .toc.h5 {
      font-size: 60%;
      text-indent: 1.85em;
    }
    .toc.h6 {
      font-size: 50%;
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
  /* prompt anchors */
  :global(a.prompt-anchor) {
    text-decoration: none;
    cursor: pointer;
  }
  :global(.prompt) :global(.prompt-anchor) { 
    display: inline-block;
    visibility: hidden;
  }
  :global(.prompt):hover :global(.prompt-anchor) {
    visibility: visible;
  }
</style>

<div class="row">
  <div class="col-sm-12 text-center">
    <div class="dropdown show">
      <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        Download Notebook
      </button>
      <div class="dropdown-menu">
        <a
          class="dropdown-item"
          href="{nbdownload}"
          title="The standalone jupyter notebook as shown"
        >Jupyter Notebook (.ipynb)</a>
        <a
          class="dropdown-item"
          href="../export/{session_id}/?format=html"
          title="An nbconvert HTML export of the notebook for easy viewing in browser"
        >HTML Export (.html)</a>
        <a
          class="dropdown-item"
          href="../export/{session_id}/?format=zip"
          title="An archive with the notebook and dependent files for running it"
        >Notebook Bundle (.zip)</a>
      </div>
    </div>
    {#if extras.indexOf('toggle-code') !== -1}
      <a
        href="javascript:"
        class="btn btn-secondary white"
        on:click={() => show_code = !show_code}
      >
        Toggle Code
      </a>
    {/if}
    {#if extras.indexOf('catalog-integration') !== -1}
    <a
      id="run-notebook-locally"
      class="btn btn-primary"
      role="button"
      class:disabled={local_run_url === undefined}
      href={local_run_url}
    >Run Locally</a>
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
            {#each toc as {h, id, textContent}}
              <a href="#{id}" class="toc h{h}">
                {textContent}
              </a>
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/if}
  {#if status === 'Loading...'}
    <div class="col-sm-12 text-center">
      <Loader />
    </div>
  {/if}
  <div
    bind:this={notebookRef}
    class="col-sm-12"
    class:col-md-9={toc !== undefined}
    class:col-xl-10={toc !== undefined}
  >
    {#if nb}
      <Cells>
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
