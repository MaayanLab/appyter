<script>
  import { tick, onMount } from 'svelte'
  import * as Cells from '../../../../components/jupyter/Cells.svelte'
  import * as Cell from '../../../../components/jupyter/Cell.svelte'
  import * as Input from '../../../../components/jupyter/Input.svelte'
  import * as Prompt from '../../../../components/jupyter/Prompt.svelte'
  import * as Source from '../../../../components/jupyter/Source.svelte'
  import * as Outputs from '../../../../components/jupyter/Outputs.svelte'
  import * as Output from '../../../../components/jupyter/Output.svelte'
  import * as Markdown from '../../../../components/jupyter/Markdown.svelte'
  import collapse from '../../../../utils/collapse'
  import any from '../../../../utils/any'

  export let requirejs
  export let nbdownload

  // get deps with requirejs
  let socket
  let _deps = undefined
  async function ensure_deps() {
    if (_deps === undefined) {
      _deps = await new Promise(
        (resolve, reject) =>
          requirejs(['socket'], function (socket, SocketIOFileUpload) {
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

  // state
  let status = 'Loading...'
  let statusBg = 'primary'
  var current_code_cell
  let started = false
  let scroll = false
  let md
  let nb

  async function setup_async_exec() {
    socket.on('status', async (value) => {
      await tick()
      status = value
      statusBg = 'primary'
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
      let { execution_count, outputs } = value
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

  onMount(async () => {
    const req = await fetch(nbdownload)
    const value = await req.json()
    nb = {...value, cells: value.cells.map((cell, index) => ({ ...cell, index })) }
    status = undefined
    // iff not run already
    // execute()
  })
</script>

<div class="row">
  <div class="col-sm-12 text-center">
    <button
      class="btn btn-primary"
      on:click={execute}
    >Execute notebook</button>
    <a
      id="download-notebook"
      class="btn btn-primary"
      role="button"
      href="{nbdownload}"
    >Download Notebook</a>
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
  <div class="col-sm-12">
    {#if nb}
      <Cells>
        {#each nb.cells as cell (cell.index)}
          {#if cell.cell_type === 'code'}
            <Cell type="code">
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
        {/each}
      </Cells>
    {/if}
  </div>
</div>
