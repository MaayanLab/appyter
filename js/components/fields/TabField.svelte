<script>
  export let args
</script>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-2 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup data-toggle="tooltip" title={args.description}><i class="far fa-question-circle"></i></sup>
    {/if}:
  </div>
  <div class="col-lg-2 pt-2 pt-lg-0">
    <div
      class="nav flex-column nav-pills nav-justified"
      aria-orientation="vertical"
      role="tablist"
    >
      {#each Array.isArray(args.choices) ? args.choices : Object.keys(args.choices) as choice_name}
        <button
          type="button"
          class="nav-link{args.value === choice_name ? ' active' : ''}"
          aria-controls="tab-content-{args.name}-{choice_name}"
          role="tab"
          on:click={() => args.value = choice_name}
        >
          {choice_name}
        </button>
      {/each}
    </div>
  </div>
  <div class="col-lg-8 pt-2 pt-lg-0">
    <div class="tab-content">
      <div
        class="tab-pane show active"
        role="tabpanel"
      >
        <slot tab={args.value}></slot>
      </div>
    </div>
  </div>
</div>
