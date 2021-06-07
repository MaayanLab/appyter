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

  let invalid = []
  $: if (value !== undefined && constraint !== undefined) {
    invalid = value
      .replace(/\n+$/g, '')
      .split('\n')
      .filter(v => constraint.exec(v) === null)
      .map((value, index) => ({ value, index }))
  }
</script>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}{#if args.description}<sup data-toggle="tooltip" title="{args.description}"><i class="far fa-question-circle"></i></sup>{/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    <textarea
      name={args.name}
      placeholder={args.hint}
      rows={args.rows}
      cols={args.cols}
      class="form-control nodecoration tiny"
      class:is-valid={invalid.length === 0}
      class:is-invalid={invalid.length !== 0}
      bind:value={value}
    ></textarea>
    <div class="invalid-feedback">
      {#each invalid as el}
        Line {el.index}: {el.value} contains unsupported characters<br />
      {/each}
      Each line should match `{args.constraint}`
    </div>
  </div>
</div>
