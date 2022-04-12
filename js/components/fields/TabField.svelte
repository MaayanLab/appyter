<script>
  import hash from '@/lib/stores/url_hash_store'
  import url_for from '@/utils/url_for'

  export let args
  $: if ($hash.params[args.name] !== undefined) {
    args.value = $hash.params[args.name]
  } else {
    $hash.params[args.name] = args.value
  }
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
        <a
          class="nav-link{args.value === choice_name ? ' active' : ''}"
          aria-controls="tab-content-{args.name}-{choice_name}"
          role="tab"
          href={`${url_for($hash.server)}#${url_for({ path: $hash.path, params: {...$hash.params, [args.name]: choice_name} })}` }
        >
          {choice_name}
        </a>
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
