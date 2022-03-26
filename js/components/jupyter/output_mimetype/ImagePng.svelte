<script>
  import collapse from '@/utils/collapse.js'
  export let data
</script>

<div class="output_png">
  <img
    class="img-fluid"
    alt="Output figure"
    src="data:img/png;base64,{collapse(data)}"
  />
</div>
