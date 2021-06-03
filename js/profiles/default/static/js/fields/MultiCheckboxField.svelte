<script>
  import ensure_list from '@/utils/ensure_list'

  export let args

  let value = {}
  if (args.default) {
    for (const k of ensure_list(args.default)) {
      value[k] = true
    }
  }

$: args.value = JSON.stringify(Object.keys(value).filter(k => value[k]))
</script>

<style>
.cursor-pointer {
  cursor: pointer;
}
</style>

<div class="row px-3 pb-3">
  <div class="col-lg-3 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup><i class="far fa-question-circle" data-toggle="tooltip" title="" data-original-title={args.description}></i></sup>
    {/if}:
  </div>
  <div class="col-lg-6 pt-2 pt-lg-0">
    <ul class="list-group multi-checkbox-field">
      {#each args.choices as choice}
        <li
          class="list-group-item cursor-pointer"
          on:click={() => value[choice] = !value[choice]}
        >
          <div class="form-check">
            <input
              id="{args.name}-{choice}-checkbox"
              type="checkbox"
              class="form-check-input"
              checked={value[choice]}
            />
            <span class="form-check-label">
              {choice}
              {#if args.descriptions && args.descriptions[choice]}
                <sup><i class="far fa-question-circle" data-toggle="tooltip" title="" data-original-title={args.descriptions[choice]}></i></sup>
              {/if}
            </span>
          </div>
        </li>
      {/each}
    </ul>
    <input
      id={args.name}
      name={args.name}
      style="display: none;"
      type="text"
      value={args.value}
    />
  </div>
</div>
