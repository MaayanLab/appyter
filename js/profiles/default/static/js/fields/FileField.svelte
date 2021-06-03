<script>
  import { onMount } from "svelte"
  import get_require from '@/utils/get_require'

  export let window
  export let args

  // file field DOM element
  let fileField

  // field state
  let state
  let filename
  let full_filename

  // setup example downloading event handlers
  async function setup_download(socket) {
    socket.on('download_queued', function (evt) {
      if (evt.name !== args.name) return
      state = {
        striped: true,
        bg: 'primary',
        progress: 0,
      }
    })
    socket.on('download_start', function (evt) {
      if (evt.name !== args.name) return
      state = {
        ...state,
        animated: true,
      }
    })
    socket.on('download_progress', function (evt) {
      if (evt.name !== args.name) return
      if (evt.total_size < 0) {
        state = {
          ...state,
          progress: 25,
          bg: 'warning',
        }
      } else if (evt.total_size === 0) {
        state = {
          ...state,
          progress: 100,
        }
      } else {
        state = {
          ...state,
          progress: (((evt.chunk * evt.chunk_size) / evt.total_size) * 100) | 0,
        }
      }
    })
    socket.on('download_complete', function (evt) {
      if (evt.name !== args.name) return
      state = {
        ...state,
        bg: 'success',
        animated: false,
        striped: false,
        progress: 100,
      }
      filename = evt.filename
      full_filename = evt.full_filename
    })
    socket.on('download_error', function (evt) {
      if (evt.name !== args.name) return
      if (evt.error === 'HTTP Error 404: Not Found') {
        state = {
          progress: 100,
          url: evt.url,
          bg: 'danger',
          error: evt.error,
          striped: false,
          animated: false,
        }
      } else {
        state = {
          progress: 100,
          url: evt.url,
          bg: 'warning',
          error: evt.error,
          striped: false,
          animated: false,
        }
      }
    })
  }

  // setup uploading event handlers
  async function setup_upload(siofu) {
    siofu.listenOnInput(fileField)
    siofu.addEventListener('start', function (evt) {
      state = {
        striped: true,
        bg: 'primary',
        progress: 0,
      }
    })
    siofu.addEventListener('progress', function (evt) {
      state = {
        ...state,
        progress: ((evt.bytesLoaded / evt.file.size) * 100) | 0,
        animated: true,
      }
    })
    siofu.addEventListener('complete', function (evt) {
      state = {
        progress: 100,
        bg: 'success',
        striped: false,
        animated: false,
      }
      filename = evt.file.name
      full_filename = evt.detail.full_filename
    })
    siofu.addEventListener('error', function (evt) {
      console.error(evt)
      state = {
        progress: 100,
        bg: 'danger',
        error: evt.error,
        striped: false,
        animated: false,
      }
    })
  }

  // trigger example download
  async function load_file(name, url, file) {
    if (url.indexOf('://') === -1) {
      url = new URL(url, document.baseURI).href
    }
    const socket = await get_require(window, 'socket')
    socket.emit('download_start', {
      name: name,
      url: new URL(url).href,
      file: file,
    })
  }

  onMount(async () => {
    window.require.config({
      paths: {
        'socketio-file-upload': `${window._config.STATIC_URL}js/lib/socketio-file-upload/client.min`,
      },
      shim: {
        'socketio-file-upload': {
          exports: 'SocketIOFileUpload'
        },
      }
    })

    const [socket, SocketIOFileUpload] = await get_require(window, ['socket', 'socketio-file-upload'])
    await setup_download(socket)
    await setup_upload(new SocketIOFileUpload(socket))
  })
</script>

<style>
.progress {
  height: 25px;
  width: 100%;
  background-color: grey;
}
.progress-bar {
  height: 100%;
  background-color: blue;
}
.progress-bar.bg-success {
  height: 100%;
  background-color: green;
}
</style>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup data-toggle="tooltip" title={args.description}><i class="far fa-question-circle"></i></sup>
    {/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    <div class="custom-file" dropzone="copy">
      <input
        bind:this={fileField}
        type="file"
        class="custom-file-input"
        id={args.name}
      />
      <input
        type="text"
        class="hidden"
        name={args.name}
        bind:value={full_filename}
      />
      <label class="custom-file-label" for={args.name}>{filename || 'Choose file'}</label>
    </div>
    {#if state !== undefined}
    <div>
      <div class="progress bg-light">
        <div
          class="progress-bar bg-{state.bg}"
          class:progress-bar-striped={state.striped}
          class:progress-bar-animated={state.animated}
          role="progressbar"
          aria-valuemin="0"
          aria-valuemax="100"
          aria-valuenow={state.progress}
          style="width: {state.progress}%"
        />
      </div>
      {#if state.error}
        <div class="alert alert-danger">
          Error downloading file: {state.error}
          {#if state.url}from <a href={state.url} target=_blank>{state.url}</a>{/if}
        </div>
      {/if}
      {#if state.warning}
        <div class="alert alert-warning">
          Error downloading file: {state.error}<br />
          <b>It may require user engagement</b>, please visit
            <a href={state.url} target=_blank>{state.url}</a>
          to download the example file for upload.
        </div>
      {/if}
    </div>
    {/if}
    {#if args.examples && Object.keys(args.examples).length > 0}
      <div class="d-table">
        <div class="d-table-row">
          <span class="d-table-cell mr-1 my-1 p-1 text-right" style="white-space: nowrap">
            Load example{#if Object.keys(args.examples).length > 1}s{/if}
            <sup data-toggle="tooltip" title="Load the example file directly into the appyter"><i class="far fa-question-circle"></i></sup>:
          </span>
          <div class="d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center">
            {#each Object.keys(args.examples) as example_name}
              <span class="text-sm m-1 p-1" style="white-space: nowrap;">
                <a
                  href="javascript:"
                  on:click={() => load_file(args.name, args.examples[example_name], example_name)}
                >{example_name}</a>
              </span>
            {/each}
          </div>
        </div>
        <div class="d-table-row">
          <span class="d-table-cell mr-1 my-1 p-1 text-right" style="white-space: nowrap">
            Download example{#if Object.keys(args.examples).length > 1}s{/if}
            <sup data-toggle="tooltip" title="Download the example file for inspection"><i class="far fa-question-circle"></i></sup>:
          </span>
          <div class="d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center">
            {#each Object.keys(args.examples) as example_name}
              <span class="text-sm m-1 p-1" style="white-space: nowrap;">
                <a
                  href={args.examples[example_name]}
                  target="_blank"
                >{example_name}</a>
              </span>
            {/each}
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
