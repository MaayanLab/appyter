<script>
  import * as OutputMimetype from '../OutputMimetype.svelte'
  export let data
</script>

<div class="output_display_data">
  <OutputMimetype data={data} />
</div>
