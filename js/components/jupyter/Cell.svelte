<script>
  export let type
  export let styles
</script>

<div class="cell border-box-sizing {type}_cell rendered" style="{styles}">
  <slot></slot>
</div>