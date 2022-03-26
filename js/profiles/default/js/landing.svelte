<script>
  import { tick, onMount } from 'svelte'
  import auth from '@/lib/stores/keycloak_auth_store'
  import hash from '@/lib/stores/url_hash_store'
  import Lazy from '@/components/Lazy.svelte'
  import Loader from '@/components/Loader.svelte'
  import { setup_chunking } from '@/lib/socketio'
  import pagehit from '@/extras/catalog-integration/pagehit'
  export let nbdownload

  const paths = window.location.pathname.split('/').filter(p => p)
  const session_id = paths[paths.length - 1]

  let nb
  let notebookRef
  let local_run_url

  // table of contents
  let toc
  onMount(() => {
    if (window._config.EXTRAS.indexOf('toc') !== -1 && notebookRef !== undefined) {
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
    const { default: socket } = await import('@/lib/socket')
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
      const req = await fetch(nbdownload, {
          cache: 'no-cache',
          headers: {
            'Authorization': $auth.state === 'auth' ? `Bearer ${$auth.keycloak.token}` : null,
          },
        })
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

    if (window._config.EXTRAS.indexOf('catalog-integration') !== -1) {
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

      pagehit(pagehit_type)
    }
  }

  let show_code = undefined
  $: if ($hash.params.show_code) {
    show_code = JSON.parse($hash.params.show_code)
  }

  let path = $hash.path // defer scroll handling for init
  $: if ($hash.path && $hash.path !== path) { // debounce scroll handling
    path = $hash.path+''
    const el = document.getElementById(path)
    if (el) el.scrollIntoView()
  }

  // initialization
  onMount(async () => {
    await tick()
    status = 'Loading...'
    statusBg = 'primary'
    if (show_code === undefined) {
      show_code = window._config.EXTRAS.indexOf('hide-code') === -1
    }
    await init()
    // trigger scroll handler
    path = undefined
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
    /* ensure menu appears over toc */
    .sticky-top {
      z-index: 1020;
    }
    .dropdown-menu {
      z-index: 1021;
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
    <div class="d-inline-block">
      <div class="dropdown">
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
    </div>
    {#if window._config.EXTRAS.indexOf('toggle-code') !== -1}
      <a
        href="javascript:"
        class="btn btn-secondary white"
        on:click={() => {
          $hash.params.show_code = JSON.stringify(!show_code)
          $hash.path = ''
        }}
      >
        Toggle Code
      </a>
    {/if}
    {#if window._config.EXTRAS.indexOf('catalog-integration') !== -1}
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
      <Lazy
        module={() => import('@/components/jupyter/Notebook.svelte')}
        props={{
          nb, show_code, current_code_cell
        }}
      />
    {/if}
  </div>
</div>
