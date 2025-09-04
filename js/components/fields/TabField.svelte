<script>
  export let args
</script>

<div class="row px-4 px-lg-3 pb-4">
  <div class="text-center mx-auto">
    {args.label}
    {#if args.description}
      <sup data-toggle="tooltip" title={args.description}><i class="far fa-question-circle"></i></sup>
    {/if}:
  </div>
  <div class="row p-4 pt-lg-0">
    <div
      class="nav flex-row nav-pills nav-justified mx-auto w-100"
      aria-orientation="horizontal"
      role="tablist"
    >
      {#each Array.isArray(args.choices) ? args.choices : Object.keys(args.choices) as choice_name}
        <button
          type="button"
          class="nav-link border{args.value === choice_name ? ' active' : ''}"
          aria-controls="tab-content-{args.name}-{choice_name}"
          role="tab"
          on:click={() => {
            if (args.value === choice_name) {
              const m = /^(.+?)-type$/.exec(args.name)
              if (m != null) {
                const el = document.querySelector(`.custom-file-input[id="${m[1]}"]`)
                if (el !== null) {
                  el.click()
                }
              }
            }
            args.value = choice_name
          }}
        >
          {choice_name}
        </button>
      {/each}
    </div>
  </div>
  <div class="col-12 pt-2 pt-lg-0 mx-auto">
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
