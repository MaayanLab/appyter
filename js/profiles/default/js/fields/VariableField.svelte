<script>
  import SSRField from '@/components/app/SSRField.svelte'
  export let args

  let fields = {}
  let id_counter = 0
  for (const value of (args.default || [])) {
    fields[id_counter++] = {
      ...args.field,
      args: {
        ...args.field.args,
        name: `${args.field.args.name}${id_counter}`,
        default: value,
      }
    }
  }
  $: args.value = JSON.stringify(
    Object.values(fields)
      .map(field => ({ '$ref': `#/${field.args.name}` }))
  )
</script>

<div class="row px-3 pb-3">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup data-toggle="tooltip" title={args.description}><i class="far fa-question-circle"></i></sup>
    {/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    {#each Object.keys(fields) as value_id (value_id)}
    <button
      type="button"
      class="btn btn-sm btn-danger"
      style="float: right"
      data-target={value_id}
      on:click={() => {
        delete fields[value_id]
        fields = fields
      }}
    ><i class="fas fa-trash text-white"></i></button>
      <SSRField
        field={fields[value_id].field}
        args={fields[value_id].args}
      />
    {/each}
    <button
      type="button"
      class="btn btn-sm btn-success"
      style="float: right"
      class:disabled={args.max && fields.length > args.max}
      disabled={args.max && fields.length > args.max}
      on:click={() => {
        if (args.max && fields.length > args.max) return
        fields[id_counter++] = {...args.field, args: {...args.field.args, name: `${args.field.args.name}${id_counter}`}}
      }}
    ><i class="fas fa-plus text-white"></i></button>
  </div>
</div>

<div style="display: none">
  <input
    type="text"
    class="hidden"
    name={args.name}
    value={args.value}
  />
</div>