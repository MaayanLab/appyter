<script>
  import auth from "@/lib/stores/keycloak_auth_store"
  import { onMount } from "svelte"

  export let args

  // file field DOM element
  let fileField

  // field state
  let state = {}
  let filenames
  let full_filenames

  $: filenames = Object.keys(state)
    .reduce((files, file) =>
      state[file].filename !== undefined ? [...files, state[file].filename] : files, [])
        .join(', ')

  $: full_filenames = Object.keys(state)
    .reduce((files, file) =>
      state[file].full_filename !== undefined ? [...files, state[file].full_filename] : files, [])
    .join('\n')

  let ctx

  // setup uploading event handlers
  async function setup_upload(siofu) {
    siofu.listenOnInput(fileField)
    siofu.addEventListener('start', function (evt) {
      evt.file.meta.auth = $auth.keycloak.token
      state = {
        ...(args.multiple ? state : {}),
        [evt.file.name]: {
          filename: evt.file.name,
          striped: true,
          bg: 'primary',
          progress: 0,
        }
      }
    })
    siofu.addEventListener('progress', function (evt) {
      if (!(evt.file.name in state)) return
      state = {
        ...state,
        [evt.file.name]: {
          ...state[evt.file.name],
          progress: ((evt.bytesLoaded / evt.file.size) * 100) | 0,
          animated: true,
        },
      }
    })
    siofu.addEventListener('complete', function (evt) {
      if (!(evt.file.name in state)) return
      state = {
        ...state,
        [evt.file.name]: {
          filename: evt.file.name,
          full_filename: evt.detail.full_filename,
          progress: 100,
          bg: 'success',
          striped: false,
          animated: false,
        }
      }
    })
    siofu.addEventListener('error', function (evt) {
      console.error(evt)
      if (!(evt.file.name in state)) return
      state = {
        ...state,
        [evt.file.name]: {
          progress: 100,
          bg: 'danger',
          error: evt.error,
          striped: false,
          animated: false,
        },
      }
    })
  }

  // trigger example download
  async function load_file(url, file) {
    state = {
      ...(args.multiple ? state : {}),
      [file]: {
        filename: file,
        striped: true,
        animated: true,
        bg: 'primary',
        progress: 0,
      }
    }
    if (url.indexOf('://') === -1) {
      url = new URL(url, document.baseURI).href
    }
    try {
      const res = await fetch(`check/${url}`)
      if (res.status !== 200) throw new Error()
      if (!(file in state)) return
      state = {
        ...state,
        [file]: {
          ...state[file],
          full_filename: `${url}#${file}`,
          bg: 'success',
          animated: false,
          striped: false,
          progress: 100,
        },
      }
    } catch (e) {
      if (!(file in state)) return
      state = {
        ...state,
        [file]: {
          ...state[file],
          progress: 100,
          url,
          bg: 'warning',
          striped: false,
          animated: false,
        },
      }
    }
  }

  onMount(async () => {
    const { default: SocketIOFileUpload } = await import('socketio-file-upload')
    const { default: socket } = await import('@/lib/socket')
    const siofu = new SocketIOFileUpload(socket)
    ctx = { socket, siofu }
    await setup_upload(siofu)
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
        multiple={args.multiple}
      />
      <textarea
        class="hidden"
        name={args.name}
        value={full_filenames}
      />
      <label class="custom-file-label" for={args.name}>{filenames || `Choose file${args.multiple ? 's' : ''}`}</label>
    </div>
    {#each Object.keys(state) as id}
      <div>
        <div class="progress bg-light">
          <div
            class="progress-bar bg-{state[id].bg}"
            class:progress-bar-striped={state[id].striped}
            class:progress-bar-animated={state[id].animated}
            role="progressbar"
            aria-valuemin="0"
            aria-valuemax="100"
            aria-valuenow={state[id].progress}
            style="width: {state[id].progress}%"
          >{state[id].filename}</div>
          <button
            type="button"
            class="btn btn-sm bg-danger text-white"
            on:click={() => {
              const { [id]: current, ...new_state } = state
              if (current.progress !== 100) {
                // TODO: abort
                // ctx.siofu.abort(id, ctx.socket)
              }
              state = new_state
            }}
          >&times;</button>
        </div>
        {#if state[id].bg === 'error'}
          <div class="alert alert-danger">
            Error loading file{#if state[id].error}: {state[id].error}{/if}
            {#if state[id].url}from <a href={state[id].url} target=_blank rel=noreferrer>{state[id].url}</a>{/if}
          </div>
        {/if}
        {#if state[id].bg === 'warning'}
          <div class="alert alert-warning">
            Error loading file{#if state[id].error}: {state[id].error}{/if}<br />
            <b>It may require user engagement</b>, please visit
              <a href={state[id].url} target=_blank rel=noreferrer>{state[id].url}</a>
            to download the example file for upload.
          </div>
        {/if}
      </div>
    {/each}
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
                <button type="button" class="text-btn"
                  on:click={() => load_file(args.examples[example_name], example_name)}
                >{example_name}</button>
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
                  target=_blank
                  rel=noreferrer
                >{example_name}</a>
              </span>
            {/each}
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
