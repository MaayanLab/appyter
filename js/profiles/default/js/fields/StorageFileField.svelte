<script>
  import auth from '@/lib/stores/keycloak_auth_store'
  export let window
  export let args

  let value = args.value || args.default || ''
  $: args.value = `${args.storage}${value}#${value.split('/').slice(-1)[0]}`

  let cwd = ''

  let parent = ''
  $: parent = cwd.split('/').slice(0, -1).join('/')

  let ls = {}
  $: if (!(cwd in ls)) {
    fetch(`StorageFileField/ls/${args.storage}${cwd}`, {
      headers: {
        'Authorization': $auth.state === 'auth' ? `Bearer ${$auth.keycloak.token}` : null,
      },
    })
      .then(res => res.json())
      .then(res => ls[cwd] = res)
      .catch(err => ls[cwd] = [])
  }

  function human_size(size) {
    let postfix = 'B'
    let precision = 0
    if (size > 1000) {
      postfix = 'KB'
      precision += 1
      size /= 1000
    }
    if (size > 1000) {
      postfix = 'MB'
      precision += 1
      size /= 1000
    }
    if (size > 1000) {
      postfix = 'GB'
      precision += 1
      size /= 1000
    }
    return `${size.toFixed(2)} ${postfix}`
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
    <h4>Browsing <code>{args.storage}</code></h4>
    <ul style="list-style: none;" class="pl-0">
      <li> [D] . {cwd}</li>
      {#if parent !== cwd}
        <li> [D] <a href="javascript:" on:click={()=>{ cwd = parent }}>.. {parent}</a></li>
      {/if}
      {#each (ls[cwd]||[]) as p}
        {#if p.type === 'directory'}
          <li> [D] <a href="javascript:" on:click={()=>{ cwd = p.name }}>{p.name}</a></li>
        {/if}
      {/each}
      {#each (ls[cwd]||[]) as p}
        {#if p.type === 'file'}
          <li> [F] <a href="javascript:" on:click={()=>{ value = p.name }}>
            {#if value === p.name}
              <b>{p.name} ({human_size(p.size)})</b>
            {:else}
              {p.name} ({human_size(p.size)})
            {/if}
          </a></li>
        {/if}
      {/each}
    </ul>
    <input
      type="text"
      style="display: none"
      name={args.name}
      bind:value={args.value}
    />
  </div>
</div>
