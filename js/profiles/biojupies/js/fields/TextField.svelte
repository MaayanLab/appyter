<script>
  import re_full from '@/utils/re_full'

  export let args

  let value
  $: if (args !== undefined && value === undefined) {
    value = args.default
  }

  let constraint
  $: if (args !== undefined) {
    constraint = re_full(args.constraint, 's')
  }

  let valid = true
  $: if (value !== undefined && constraint !== undefined) {
    valid = constraint.exec(value) !== null
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
      class:is-valid={valid}
      class:is-invalid={!valid}
      bind:value={value}
    ></textarea>
    <div class="invalid-feedback">
      String contains unsupported characters (should match `{args.constraint}`).
    </div>
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
  </div>
</div>