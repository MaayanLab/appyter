<script>
  import * as AppyterField from '../../../../../components/AppyterField.svelte';
  export let args

  let values = {}
  let id_counter = 0
  for (const v of (args.default || [])) {
    values[id_counter++] = {...v, args: {...v.args, name: `${v.args.name}_${id_counter}`}}
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
    {#each Object.keys(values) as value_id (value_id)}
    <a
      href="javascript:"
      class="btn btn-sm btn-danger"
      style="float: right"
      data-target={value_id}
      on:click={() => {
        delete values[value_id]
        values = values
      }}
    ><i class="fas fa-trash text-white"></i></a>
      <AppyterField
        data={values[value_id]}
      />
    {/each}
    <a
      href="javascript:"
      class="btn btn-sm btn-success"
      style="float: right"
      class:disabled={args.max && values.length > args.max}
      disabled={args.max && values.length > args.max}
      on:click={() => {
        if (args.max && values.length > args.max) return
        values[id_counter++] = {...args.field, args: {...args.field.args, name: `${args.field.args.name}_${id_counter}`}}
      }}
    ><i class="fas fa-plus text-white"></i></a>
  </div>
</div>

<div style="display: none">
  <input
    type="text"
    class="hidden"
    name={args.name}
    value={JSON.stringify(Object.keys(values).map((v) => v.args.name))}
  />
  <AppyterField
    data={{...args.field, args: {...args.field.args, value: ''}}}
  />
</div>