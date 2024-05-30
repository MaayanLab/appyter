<script>
  import Lazy from "@/components/Lazy.svelte";
  import hash from "@/lib/stores/url_hash_store";
  import Cell from "@/components/jupyter/Cell.svelte";
  import Input from "@/components/jupyter/Input.svelte";
  import Prompt from "@/components/jupyter/Prompt.svelte";
  import Source from "@/components/jupyter/Source.svelte";
  import Outputs from "@/components/jupyter/Outputs.svelte";

  import collapse from "@/utils/collapse";
  import any from "@/utils/any";

  export let nb;
  export let show_code;
  export let current_code_cell;
  export let nbdownload;

  const paths = window.location.pathname.split("/").filter((p) => p);
  const instance_id = paths[paths.length - 1];
</script>

<Lazy module={() => import("@/components/jupyter/Cells.svelte")} children>
  {#each nb.cells as cell (cell.index)}
    {#if collapse(cell.source) !== ""}
      {#if cell.cell_type === "code"}
        <Cell type="code" outputs="{cell.outputs.length}">
          {#if show_code}
            <Input>
              <Prompt
                prompt_type="input"
                index={cell.index}
                running={current_code_cell !== undefined
                  ? cell.index >= current_code_cell
                  : undefined}
                error={any(
                  cell.outputs.map(({ output_type }) => output_type === "error")
                )}
                counter={cell.execution_count}
                cell_type={cell.cell_type}
              />
              <Source language="python" source={collapse(cell.source)} />
            </Input>
          {/if}
          <Outputs
            index={cell.index}
            data={cell.outputs || []}
            loading={current_code_cell}
          />
        </Cell>
        {#if "buttons" in cell.metadata}
          <div class="col-sm-12 text-center p-3">
            <div class="d-inline-block">
              <div class="dropdown">
                <button
                  type="button"
                  class="btn btn-primary dropdown-toggle"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  Download As
                </button>
                <div class="dropdown-menu">
                  <a
                    class="dropdown-item"
                    href={`${nbdownload}${window.location.search}`}
                    title="The standalone jupyter notebook as shown"
                    >Jupyter Notebook (.ipynb)</a
                  >
                  <a
                    class="dropdown-item"
                    href={`../export/${instance_id}/${window.location.search ? `${window.location.search}&` : "?"}format=html`}
                    title="An nbconvert HTML export of the notebook for easy viewing in browser"
                    >HTML Export (.html)</a
                  >
                  <a
                    class="dropdown-item"
                    href={`../export/${instance_id}/${window.location.search ? `${window.location.search}&` : "?"}format=zip`}
                    title="An archive with the notebook and dependent files for running it"
                    >Notebook Bundle (.zip)</a
                  >
                  <a
                    class="dropdown-item"
                    href={`../export/${instance_id}/${window.location.search ? `${window.location.search}&` : "?"}format=pdf`}
                    title="An archive with the notebook and dependent files for running it"
                    >PDF Export (.pdf)</a
                  >
                </div>
              </div>
            </div>
            <button
              type="button"
              class="btn btn-secondary white"
              on:click={() => {
                $hash.params.show_code = JSON.stringify(!show_code);
                $hash.path = "";
              }}
            >
              Toggle Code
            </button>
            <button
              type="button"
              class="btn btn-dark white"
              style="color: white !important;"
              onclick="downloadCitation()"
            >
              Export Citation
            </button>
            <a
              class="share-item"
              title="Copy the link to this report"
              href="#top"
              on:click={() => {
                navigator.clipboard.writeText(window.location.href);
              }}
            >
              <img src="/static/share.png" alt="Share" width="30px" />
            </a>
            <a
              class="share-item"
              href={`https://www.linkedin.com/shareArticle?mini=true&url=https%3A//${window.location.host + window.location.pathname}`}
              title="Share a link to the report on LinkedIn"
              target="_blank"
              ><img src="/static/linkedin.png" alt="LinkedIn" width="30px" />
            </a>
            <a
              class="share-item"
              href={`https://twitter.com/intent/tweet?text=https%3A//${window.location.host + window.location.pathname}`}
              title="Share a link to the report on X"
              target="_blank"
              ><img src="/static/X.png" alt="X" width="30px" />
            </a>
          </div>
        {/if}
      {:else if cell.cell_type === "markdown"}
        <Cell type="text">
          <Input>
            <Prompt prompt_type="input" index={cell.index} />
            <div class="inner_cell">
              <div class="text_cell_render border-box-sizing rendered_html">
                <Lazy
                  module={() => import("@/components/Markdown.svelte")}
                  props={{ data: collapse(cell.source) }}
                />
              </div>
            </div>
          </Input>
        </Cell>
      {/if}
    {/if}
  {/each}
</Lazy>
