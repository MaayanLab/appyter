<script>
  import { onMount } from 'svelte'
  import Loader from '@/components/Loader.svelte'

  export let args
  let focused
  let error
  let value
  let items
  let current_focus = -1
  let relevant_items

  $: if (args !== undefined && value === undefined) {
    value = args.default
  }

  $: if (items !== undefined) {
    relevant_items = Object.keys(items)
      .filter(item => item.toLowerCase().substr(0, value.length) === value.toLowerCase() && item !== value)
      .slice(0, 7)
    current_focus = -1
  }

  function set(arr) {
    const s = {}
    for (const v of arr) s[v]=true
    return s
  }

  onMount(async () => {
    try {
      if (args.file_path !== undefined) {
        const req = await fetch(args.file_path)
        const result = await req.json()
        if (typeof result !== 'object') {
          throw new Error('Unrecognized type for downloaded file')
        } else if (Array.isArray(result)) {
          items = set(result)
        } else {
          console.warn('Legacy mode... please use an array')
          items = set(result[Object.keys(result)[0]])
        }
      } else if (args.choices !== undefined) {
        if (typeof args.choices !== 'object') {
          throw new Error('Unrecognized type for choices')
        } else if (Array.isArray(args.choices)) {
          items = set(args.choices)
        } else {
          items = args.choices
        }
      } else {
        throw new Error('No autocomplete item source')
      }
    } catch(e) {
      error = 'Failed to load autocomplete items'
      console.error(e)
    }
  })
</script>

<style>
.autocomplete {
  position: relative;
  display: inline-block;
}

.autocomplete-items {
  background-color: white;
  position: absolute;
  border: 1px solid #d4d4d4;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /*position the autocomplete items to be the same width as the container:*/
  top: 100%;
  left: 0;
  right: 0;
}

.autocomplete-items div {
  padding: 10px;
  cursor: pointer;
  background-color: #fff; 
  border-bottom: 1px solid #d4d4d4; 
}

.autocomplete-items div:hover {
  background-color: #e9e9e9; 
}

.autocomplete-active {
  background-color: DodgerBlue !important; 
  color: #ffffff; 
}
</style>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup><i class="far fa-question-circle" data-toggle="tooltip" title="" data-original-title={args.description}></i></sup>
    {/if}:
  </div>
  <div class="autocomplete col-lg-6 pt-2 pt-lg-0">
    <input
      type="text"
      id={args.name}
      name={args.name}
      class="form-control nodecoration tiny bg-white px-2 py-1 mb-0"
      class:is-valid={items !== undefined && items[value] !== undefined}
      class:is-invalid={focused === false && items !== undefined && items[value] === undefined}
      autocomplete="off"
      placeholder={args.hint}
      bind:value={value}
      on:focus={() => focused = true}
      on:blur={() => focused = false}
      on:keydown={(e) => {
        if (e.key === 'ArrowUp') {
          e.preventDefault()
          current_focus = Math.max(-1, current_focus - 1)
        } else if (e.key === 'ArrowDown') {
          e.preventDefault()
          current_focus = Math.min(relevant_items.length-1, current_focus + 1)
        } else if (e.key === 'Enter') {
          e.preventDefault()
          if (current_focus >= 0) value = relevant_items[current_focus]
          current_focus = -1
        }
      }}
    />
    {#if items !== undefined}
      <div class="invalid-feedback">
        Value should be selected from autocomplete results.
      </div>
    {/if}
    {#if error === undefined}
      {#if focused && value}
        <div class="autocomplete-items">
          {#if items === undefined}
            <center>
              <Loader />
            </center>
          {:else}
            {#each relevant_items as item, ind}
              <div
                class:autocomplete-active={current_focus === ind}
                on:mousedown={() => value = item}
              >
                <strong>{item.substr(0, value.length)}</strong>{item.substr(value.length)}
              </div>
            {/each}
          {/if}
        </div>
      {/if}
      {#if args.examples && Object.keys(args.examples).length > 0}
        <div class="d-table-row">
          <span class="d-table-cell mr-1 my-1 p-1 text-right" style="white-space: nowrap">
            Try example{#if Object.keys(args.examples).length > 1}s{/if}:
          </span>
          <div class="d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center">
            {#each Object.keys(args.examples) as example_name}
              <span class="text-sm m-1 p-1" style="white-space: nowrap;">
                <button type="button" class="text-btn"
                  on:click={() => value = args.examples[example_name]}
                >{Array.isArray(args.examples) ? args.examples[example_name] : example_name}</button>
              </span>
            {/each}
          </div>
        </div>
      {/if}
    {:else}
      <div class="w-100">
        <div class="alert alert-warning" role="alert">
          {error}
        </div>
      </div>
    {/if}
  </div>
</div>
