<script>
  import OutputMimetype from '@/components/jupyter/OutputMimetype.svelte'
  export let data
</script>

<div class="output_display_data">
  <OutputMimetype data={data} />
</div>
