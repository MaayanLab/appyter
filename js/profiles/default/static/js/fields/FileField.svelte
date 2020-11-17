<script>
  import { onMount } from "svelte";

  export let window
  export let args

  // get deps with requirejs
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
  let socket
  let siofu
  let _deps = undefined
  async function ensure_deps() {
    if (_deps === undefined) {
      _deps = await new Promise(
        (resolve, reject) =>
          window.require(['socket', 'socketio-file-upload'], function (socket, SocketIOFileUpload) {
            resolve({
              socket,
              siofu: new SocketIOFileUpload(socket),
            })
          }, reject)
      )
      socket = _deps.socket
      siofu = _deps.siofu
    }
  }

  // file field DOM element
  let fileField

  // field state
  let state
  let filename
  let full_filename

  // setup example downloading event handlers
  async function setup_download() {
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
        }
      } else {
        state = {
          progress: 100,
          url: evt.url,
          bg: 'warning',
          error: evt.error,
        }
      }
    })
  }

  // setup uploading event handlers
  async function setup_upload() {
    siofu.listenOnInput(fileField)
    siofu.addEventListener('start', function (evt) {
      state = {
        striped: true,
        animated: true,
        bg: 'primary',
        progress: 0,
      }
    })
    siofu.addEventListener('progress', function (evt) {
      state = {
        ...state,
        progress: ((evt.bytesLoaded / evt.file.size) * 100) | 0,
      }
    })
    siofu.addEventListener('complete', function (evt) {
      state = {
        progress: 100,
        bg: 'success',
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
      }
    })
  }

  // trigger example download
  async function load_file(name, url, file) {
    if (url.indexOf('://') === -1) {
      url = new URL(url, document.baseURI).href
    }
    await ensure_deps()
    socket.emit('download_start', {
      name: name,
      url: new URL(url).href,
      file: file,
    })
  }

  onMount(async () => {
    await ensure_deps()
    await setup_download()
    await setup_upload()
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
      <sup  data-toggle="tooltip" title={args.description}><i class="far fa-question-circle ml-1"></i></sup>
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
    {#if args.examples}
      <ul style="list-style-type: none">
        <span>Load example:</span>
        {#each Object.keys(args.examples) as example_name}
          <li style="display: inline">
            &nbsp;
            <a
              href="javascript:"
              on:click={() => load_file(args.name, args.examples[example_name], example_name)}
            >{example_name}</a>
            &nbsp;
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
