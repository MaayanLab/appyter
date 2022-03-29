<script>
  export let toc
</script>

<style>
  .toc {
    display: block;
    font-weight: bold;
  }
  .toc.h1 {
    font-size: 100%;
    text-indent: 0em;
  }
  .toc.h2 {
    font-size: 90%;
    text-indent: 1em;
  }
  .toc.h3 {
    font-size: 80%;
    text-indent: 1.5em;
  }
  .toc.h4 {
    font-size: 70%;
    text-indent: 1.75em;
  }
  .toc.h5 {
    font-size: 60%;
    text-indent: 1.85em;
  }
  .toc.h6 {
    font-size: 50%;
    text-indent: 2em;
  }
  .sticky-top {
    z-index: 1020;
  }
</style>

{#if toc !== undefined}
  <div class="col-sm-12 col-md-3 col-xl-2">
    <div class="row sticky-top">
      <div class="offset-sm-2 col-sm-8 col-md-12">
        <div class="mt-5">
          <legend>Table Of Contents</legend>
          {#each toc as {h, id, textContent}}
            <a href="#{id}" class="toc h{h}">
              {textContent}
            </a>
          {/each}
        </div>
      </div>
    </div>
  </div>
{/if}
