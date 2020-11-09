<script>
  import * as HTML from '../../../../../components/HTML.svelte';
  export let args
</script>

<div class="row px-4 px-lg-3 pb-4">
  <div class="col-lg-2 bold text-lg-right my-auto">
    {args.label}
    {#if args.description}
      <sup><i class="far fa-question-circle ml-1" data-toggle="tooltip" title="" data-original-title="{args.description}"></i></sup>
    {/if}:
  </div>
  <div class="col-lg-2 pt-2 pt-lg-0">
    <div
      class="nav flex-column nav-pills nav-justified"
      aria-orientation="vertical"
      role="tablist"
    >
      {#each Object.keys(args.choices) as choice_name}
        <a
          href="javascript:"
          class="nav-link{args.value == choice_name ? ' active' : ''}"
          aria-controls="tab-content-{args.name}-{choice_name}"
          data-toggle="tab"
          role="tab"
          on:click={() => args.value = choice_name}
       >
          {choice_name}
       </a>
      {/each}
    </div>
  </div>
  <div class="col-lg-8 pt-2 pt-lg-0">
    <div class="tab-content">
      {#each Object.keys(args.choices) as choice_name}
        <div
          class="tab-pane fade{args.value == choice_name ? ' show active' : ''}"
          role="tabpanel"
        >
          {#each args.choices[choice_name] as item (item.args.name)}
            <HTML data={args.field_renders[item.args.name]} />
          {/each}
        </div>
      {/each}
    </div>
  </div>
  <input
    type="text"
    class="hidden"
    name={args.name}
    value={args.value}
  />
</div>
