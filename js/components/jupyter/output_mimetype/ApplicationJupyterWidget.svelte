<script>
  import HTML from '@/components/HTML.svelte'
  import collapse from '@/utils/collapse.js'
  export let data
</script>

<HTML
  classes="output_widget_view"
  data='<script type="application/vnd.jupyter.widget-view+json">{JSON.stringify(collapse(data))}</script>'
/>
