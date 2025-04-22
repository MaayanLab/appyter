<script>
  import HTML from '@/components/HTML.svelte'
  import collapse from '@/utils/collapse.js'
  export let data
</script>

<div class="output_widget_view">
  <HTML
    data='<script type="application/vnd.jupyter.widget-view+json">{JSON.stringify(collapse(data))}</script>'
  />
</div>
