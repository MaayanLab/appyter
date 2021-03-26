<script>
  import * as HTML from '../../HTML.svelte'
  import collapse from '../../../utils/collapse.js'
  export let data
</script>

<HTML
  classes="output_html rendered_html"
  data={collapse(data)}
/>
