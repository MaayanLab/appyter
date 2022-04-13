<script>
  import auth from '@/lib/stores/keycloak_auth_store'
  import auth_headers from '@/utils/auth_headers'
  import Loader from '@/components/Loader.svelte'
  import human_size from '@/utils/human_size'
  export let args
  export let backend = 'StorageFileField'

  let value = args.value || args.default || ''
  $: args.value = `${args.storage}${value}#${value.split('/').slice(-1)[0]}`

  let loading = false

  let cwd = ''

  let parent = ''
  $: parent = cwd.split('/').slice(0, -1).join('/')

  let ls = {}
  $: if (!(cwd in ls)) {
    loading = true
    auth_headers($auth)
      .then(async (headers) => {
        try {
          const res = await fetch(`${backend}/ls/${args.storage}${cwd}`, { headers })
          ls[cwd] = await res.json()
          loading = false
        } catch (e) {
          ls[cwd] = []
          loading = false
        }
      })
  }
</script>

<style>
</style>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup data-toggle="tooltip" title={args.description}><i class="far fa-question-circle"></i></sup>
    {/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    <div style="display: flex; flex-direction: row; max-height: 500px; overflow-x: hidden; overflow-y: auto;" class="pl-0">
      <div style="display: flex; flex-direction: column; align-items: center; padding-right: 5px">
        {#if parent !== cwd}
          <span><i class="far fa-folder"></i> </span>
        {/if}
        <span><i class="far fa-folder-open"></i> </span>
      {#each (ls[cwd]||[]) as p}
        {#if p.type === 'directory'}
          <span><i class="far fa-folder"></i> </span>
        {/if}
      {/each}
      {#each (ls[cwd]||[]) as p}
        {#if p.type === 'file'}
          <span><i class="far fa-file"></i> </span>
        {/if}
      {/each}
      </div>
      <div style="display: flex; flex-direction: column; align-items: start; white-space: nowrap; overflow-x: auto; flex: 1 1 auto;">
        {#if parent !== cwd}
          <button type="button" class="text-btn" on:click={()=>{ cwd = parent }}>.. {parent}</button>
        {/if}
        <button type="button" class="text-btn">. {cwd}</button>
        {#each (ls[cwd]||[]) as p}
          {#if p.type === 'directory'}
            <button type="button" class="text-btn" on:click={()=>{ cwd = p.name }}>{p.name.slice(cwd.length).replace(/^\//, '')}</button>
          {/if}
        {/each}
        {#each (ls[cwd]||[]) as p}
          {#if p.type === 'file'}
            <button type="button" class="text-btn" on:click={()=>{ value = p.name }}>
              {#if value === p.name}
                <span style="font-weight: 600">{p.name.slice(cwd.length).replace(/^\//, '')}</span>
              {:else}
                {p.name.slice(cwd.length).replace(/^\//, '')}
              {/if}
            </button>
          {/if}
        {/each}
        {#if loading}
          <Loader />
        {/if}
      </div>
      <div style="display: flex; flex-direction: column; align-items: start; padding-left: 5px">
        {#if parent !== cwd}
          <span>&nbsp;</span>
        {/if}
        <span>&nbsp;</span>
        {#each (ls[cwd]||[]) as p}
          {#if p.type === 'directory'}
            <span>&nbsp;</span>
          {/if}
        {/each}
        {#each (ls[cwd]||[]) as p}
          {#if p.type === 'file'}
            {#if value === p.name}
              <span style="white-space: nowrap; font-weight: 600">{human_size(p.size)}</span>
            {:else}
              <span style="white-space: nowrap">{human_size(p.size)}</span>
            {/if}
          {/if}
        {/each}
      </div>
    </div>
    <input
      type="text"
      style="display: none"
      name={args.name}
      bind:value={args.value}
    />
  </div>
</div>
