<script>
  import { tick, onMount } from 'svelte'
  import * as Cells from '../../../../components/jupyter/Cells.svelte'
  import * as Cell from '../../../../components/jupyter/Cell.svelte'
  import * as Input from '../../../../components/jupyter/Input.svelte'
  import * as Prompt from '../../../../components/jupyter/Prompt.svelte'
  import * as Source from '../../../../components/jupyter/Source.svelte'
  import * as Outputs from '../../../../components/jupyter/Outputs.svelte'
  import * as Output from '../../../../components/jupyter/Output.svelte'
  import * as Markdown from '../../../../components/Markdown.svelte'

  export let requirejs
  export let nbdownload
  export let data

  // get deps with requirejs
  let socket
  let _deps = undefined
  async function ensure_deps() {
    if (_deps === undefined) {
      _deps = await new Promise(
        (resolve, reject) =>
          requirejs(['socket'], function (socket, SocketIOFileUpload) {
            resolve({
              socket,
            })
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

  function *reduce_output_streams(outputs) {
    let streams = {}
    for (const output of outputs) {
      if (output.output_type === 'stream') {
        if (streams[output.name] === undefined) {
          streams[output.name] = output
        } else {
          if (output.text.startsWith('\r')) streams[output.name].text = output.text
          else streams[output.name].text += output.text
        }
      } else {
        yield output
      }
    }
    for (const stream in streams) {
      yield streams[stream]
    }
  }

  async function setup_async_exec() {
    current_code_cell = 1
    socket.on('status', async (value) => {
      await tick()
      status = value
      statusBg = 'primary'
    })
    socket.on('redirect', async (value) => {
      window.location.replace(value)
    })
    socket.on('error', async (value) => {
      await tick()
      status = `Error: ${value}`
      statusBg = 'danger'
    })
    socket.on('nb', async (value) => {
      await tick()
      value.cells = value.cells.map(({ source, ...cell}, index) => ({...cell, source: source.join(''), index}))
      nb = value
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
      nb.cells[cell_index] = {...nb.cells[cell_index], execution_count, outputs: [...reduce_output_streams(outputs)] }
    })
  }

  onMount(async () => {
    await ensure_deps()
    await ensure_connected()
    await setup_async_exec()

    socket.emit('init', data)
  })
</script>

<div class="row">
  <div class="col-sm-12 text-center">
    <a
      id="download-notebook"
      class="btn btn-primary"
      role="button"
      href="{nbdownload}"
    >Download Notebook</a>
  </div>
  <div class="w-100">&nbsp;</div>
  <div class="col-sm-8 offset-sm-2">
    <div class="alert alert-{statusBg}" role="alert">
      {status}
    </div>
  </div>
  <div class="w-100"></div>
  <div class="col-sm-12">
    {#if nb}
      <Cells>
        {#each nb.cells as cell (cell.index)}
          {#if cell.cell_type == 'code'}
            <Cell type="code">
              <Input>
                <Prompt
                  running={current_code_cell === cell.index}
                  counter={cell.execution_count}
                />
                <Source
                  language="python"
                  source={cell.source}
                />
              </Input>
              <Outputs>
                {#each cell.outputs as cell_output}
                  <Output data={cell_output} />
                {/each}
              </Outputs>
            </Cell>
          {:else if cell.cell_type === 'markdown'}
            <Cell type="text">
              <Input>
                <Prompt />
                <div class="inner_cell">
                  <div class="text_cell_render border-box-sizing rendered_html">
                    <Markdown data={cell.source} />
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
