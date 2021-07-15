<script>
  import ensure_list from '@/utils/ensure_list'
  import re_full from '@/utils/re_full'

  export let args

  let value
  $: if (args !== undefined && value === undefined) {
    value = ensure_list(args.default).join('\n')
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
    {#if args.examples && Object.keys(args.examples).length > 0}
      <div class="d-table-row">
        <span class="d-table-cell mr-1 my-1 p-1 text-right" style="white-space: nowrap">
          Try example{#if Object.keys(args.examples).length > 1}s{/if}:
        </span>
        <div class="d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center">
          {#each Object.keys(args.examples) as example_name}
            <span class="text-sm m-1 p-1" style="white-space: nowrap;">
              <a
                href="javascript:"
                on:click={() => value = args.examples[example_name].join('\n')}
              >{example_name}</a>
            </span>
          {/each}
        </div>
      </div>
    {/if}
  </div>
</div>
