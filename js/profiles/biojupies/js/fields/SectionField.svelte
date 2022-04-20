<script>
  import SSRField from '@/components/app/SSRField.svelte'
  export let fields
  export let args

  function url_for(directory, path) {
    return `${window._config.ORIGIN}/${directory}/${path}`
  }
</script>

<div class="row">
  <div class="col-sm-12">
    <div class="mt-3 mb-0 w-100 border-custom rounded bg-lightgrey" data-toggle="collapse" data-target="#{args.name}">
      <div class="d-table w-100 py-2 px-2 py-md-0 px-md-0">
        <div class="d-table-cell align-middle card-icon px-3 py-3 text-center">
          {#if args.img}
            <img src="{url_for('static', args.img)}" alt="Section icon" class="w-100 px-1 py-1 rounded bg-white border-grey">
          {:else if args.icon}
            <i class="fas fa-{args.icon} fa-2x" />
          {/if}
        </div>
        <div class="d-table-cell align-middle">
          <div class="very-small regular pb-2 pr-5">{args.title}</div>
          {#if args.subtitle}<div class="tiny light text-muted">{args.subtitle}</div>{/if}
        </div>
      </div>
    </div>
    <div id="{args.name}" class="border-grey mx-2 border-top-0 rounded-bottom tiny collapse show">
      <div class="pt-3">
        {#each fields as field}
          <SSRField {...field} />
          {#if field.error !== undefined}
            <div class="alert alert-danger mx-4">
              {field.error.message}
            </div>
          {/if}
        {/each}
      </div>
    </div>
  </div>
</div>