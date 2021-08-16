<script>
  import OutputMimetype from '@/components/jupyter/OutputMimetype.svelte'
  export let data
</script>

<div class="output_execute_result">
  <OutputMimetype data={data} />
</div>
