<script>
  import * as HTML from '../../../../../components/HTML.svelte';
  export let args

  let values = {}
  let next_id = 0
  for (const value of (args.default || [])) {
    values[next_id] = { id: next_id, value }
    next_id += 1;
  }
</script>

<div class="row px-3 pb-3">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup data-toggle="tooltip" title={args.description}><i class="far fa-question-circle"></i></sup>
    {/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    {#each Object.keys(values) as value_id}
    <a
      href="javascript:"
      class="btn btn-sm btn-danger"
      style="float: right"
      on:click={() => {
        delete values[value_id]
        values = values
      }}
    ><i class="fas fa-trash text-white"></i></a>
      <HTML data={args.field_render.replace(args.field_render.name)} />
    {/each}
    <a
      href="javascript:"
      class="btn btn-sm btn-success"
      style="float: right"
      class:disabled={args.max && Object.keys(values).length > args.max}
      disabled={args.max && Object.keys(values).length > args.max}
      on:click={() => {
        if (args.max && Object.keys(values).length > args.max) return
        values[next_id] = { id: next_id, value: "test" }
        next_id += 1
      }}
    ><i class="fas fa-plus text-white"></i></a>
  </div>
</div>
