<script>
  import re_full from '@/utils/re_full'

  export let args

  let value
  $: if (args !== undefined && value === undefined) {
    value = args.default
  }

  let constraint
  $: if (args !== undefined) {
    constraint = re_full(args.constraint)
  }

  let valid = true
  $: if (value !== undefined && constraint !== undefined) {
    valid = constraint.exec(value) !== null
  }
</script>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}{#if args.description}<sup data-toggle="tooltip" title={args.description}><i class="far fa-question-circle"></i></sup>{/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    <input
      type="text"
      name={args.name}
      class="form-control nodecoration tiny bg-white px-2 py-1 mb-0"
      class:is-valid={valid}
      class:is-invalid={!valid}
      placeholder={args.hint}
      bind:value={value}
    />
    <div class="invalid-feedback">
      String contains unsupported characters (should match `{args.constraint}`).
    </div>
  </div>
</div>
