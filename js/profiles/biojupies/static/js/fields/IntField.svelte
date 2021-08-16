<script>
  import is_null from '@/utils/null'

  export let args

  let value
  $: if (args !== undefined && value === undefined) {
    value = args.default
  }

  let valid = true
  $: if (value !== undefined && args !== undefined) {
    valid =
      (value|0) === value
      && (is_null(args.min) || ((value|0) >= args.min))
      && (is_null(args.max) || ((value|0) <= args.max))
  }
</script>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}{#if args.description}<sup data-toggle="tooltip" title="{args.description}"><i class="far fa-question-circle"></i></sup>{/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    <input
      type="number"
      name="{args.name}"
      class="form-control nodecoration tiny bg-white px-2 py-1 mb-0"
      class:is-valid={valid}
      class:is-invalid={!valid}
      placeholder="{args.hint}"
      min={args.min}
      max={args.max}
      step={args.step}
      bind:value={value}
    />
    <div class="invalid-feedback">
      Value should be an integer
      {#if !is_null(args.min) && !is_null(args.max)}
        greater than or equal to {args.min} and less than or equal to {args.max}
      {:else if !is_null(args.min)}
        greater than or equal to {args.min}
      {:else if !is_null(args.max)}
        less than or equal to {args.max}
      {/if}
    </div>
  </div>
</div>
