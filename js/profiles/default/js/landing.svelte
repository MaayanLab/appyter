<script>
  import { tick, onMount } from "svelte";
  import auth from "@/lib/stores/keycloak_auth_store";
  import hash from "@/lib/stores/url_hash_store";
  import Lazy from "@/components/Lazy.svelte";
  import Loader from "@/components/Loader.svelte";
  import setup_chunking from "@/lib/socketio";
  import pagehit from "@/extras/catalog-integration/pagehit";
  import toc from "@/extras/catalog-integration/toc";
  import auth_headers from "@/utils/auth_headers";
  export let nbdownload;

  const paths = window.location.pathname.split("/").filter((p) => p);
  const instance_id = paths[paths.length - 1];

  let nb;
  let notebookRef;
  let local_run_url;

  // store notebook in config for error reporting
  $: if (nb) {
    Object.assign(window._config, { nb });
  }

  // table of contents
  $: if (window._config.EXTRAS.indexOf("toc") !== -1) toc.attach(notebookRef);

  // dynamic notebook
  let status = "Loading...";
  let statusBg = "primary";
  var current_code_cell;

  async function setup_async_exec(socket) {
    socket.on("connect", async () => {
      await tick();
      status = `Connected to server, re-initializing...`;
      statusBg = "warning";
      await init();
    });
    socket.on("reconnect", async () => {
      await tick();
      status = `Reconnecting to server...`;
      statusBg = "warning";
    });
    socket.on("disconnect", async (reason) => {
      if (reason !== "io client disconnect") {
        await tick();
        status = `Disconnected from server...`;
        statusBg = "danger";
      }
    });
    socket.on("status", async (value) => {
      await tick();
      status = value;
      statusBg = "primary";
      if (status === "Success") {
        current_code_cell = undefined;
      }
    });
    socket.on("error", async (value) => {
      await tick();
      current_code_cell = undefined;
      status = `Error: ${value}`;
      statusBg = "danger";
    });
    socket.on("nb", async (value) => {
      await tick();
      nb = {
        ...value,
        cells: value.cells.map((cell, index) => ({ ...cell, index })),
      };
    });
    socket.on("progress", async (value) => {
      await tick();
      current_code_cell = value;
    });
    socket.on("cell", async (value_index) => {
      let value = value_index[0];
      let cell_index = value_index[1];
      await tick();
      nb.cells[cell_index] = { ...nb.cells[cell_index], ...value };
    });
    setup_chunking(socket);
  }

  let connect_init = false;
  async function connect(execute) {
    const { default: socket } = await import("@/lib/socket");
    if (!connect_init) {
      connect_init = true;
      // ensure we're connected
      await new Promise((resolve, reject) => {
        if (socket.connected) resolve();
        else socket.on("connect", resolve);
      });
      await setup_async_exec(socket);
    }
    const evt = execute ? "submit" : "join";
    socket.emit(evt, {
      _id: instance_id,
      _auth: $auth.keycloak.token,
      _storage: $hash.server.params.storage,
      _executor: $hash.server.params.executor,
    });
  }

  async function init() {
    let pagehit_type = "view";
    try {
      // Load notebook
      // https://developer.mozilla.org/en-US/docs/Web/API/Request/cache
      // no-cache implies a check with the remote server no matter what, it still uses the cache if the resource hasn't changed
      const req = await fetch(`${nbdownload}${window.location.search}`, {
        cache: "no-cache",
        headers: await auth_headers($auth),
      });
      if (req.status === 404) {
        throw new Error("Notebook not found");
      }
      const value = await req.json();
      if (value.metadata.appyter === undefined) {
        console.warn("Converting legacy metadata");
        value.metadata.appyter = {
          nbconstruct: {},
        };
        if (value.metadata.execution_info !== undefined) {
          value.metadata.appyter.nbexecute = {
            started: value.metadata.execution_info.started,
            completed: value.metadata.execution_info.completed,
          };
        }
      }
      if (nb === undefined) {
        nb = {
          ...value,
          cells: value.cells.map((cell, index) => ({ ...cell, index })),
        };
      }

      if (value.metadata.appyter.nbexecute === undefined) {
        // Execute notebook if it hasn't already been executed
        await connect(true);
        pagehit_type = "execute";
      } else {
        if (value.metadata.appyter.nbexecute.completed === undefined) {
          // Notebook started but hasn't completed
          await connect(false);
          await tick();
          status = "Notebook is currently executing, joining session...";
          statusBg = "primary";
        } else {
          await tick();
          status = undefined;
          nb = {
            ...value,
            cells: value.cells.map((cell, index) => ({ ...cell, index })),
          };
        }
      }
    } catch (e) {
      await tick();
      status = `${e}`;
      statusBg = "danger";
    }

    if (window._config.EXTRAS.indexOf("catalog-integration") !== -1) {
      // setup local run appyter link
      try {
        const slug = paths[paths.length - 2] || "";

        let appyter_version = "";
        if (nb.metadata.appyter.info !== undefined)
          appyter_version = nb.metadata.appyter.info.version || "";

        let library_version = "";
        if (nb.metadata.appyter.nbexecute !== undefined)
          library_version = nb.metadata.appyter.nbexecute.version || "";
        else if (nb.metadata.appyter.nbconstruct !== undefined)
          library_version = nb.metadata.appyter.nbconstruct.version || "";

        local_run_url = `${window._config.CATALOG_ORIGIN}/#/running-appyters/?slug=${slug}&appyter_version=${appyter_version}&library_version=${library_version}&id=${instance_id}`;
      } catch (e) {
        console.error("catalog-integration: local_run_url setup error");
        console.error(e);
      }

      pagehit(pagehit_type);
    }
  }

  let show_code = undefined;
  $: if ($hash.params.show_code) {
    show_code = JSON.parse($hash.params.show_code);
  }

  let path = $hash.path; // defer scroll handling for init
  $: if ($hash.path && $hash.path !== path) {
    // debounce scroll handling
    path = $hash.path + "";
    const el = document.getElementById(path);
    if (el) el.scrollIntoView();
  }

  // initialization
  $: if ($auth.state !== "init") {
    init().then(() => {
      // trigger scroll handler
      path = undefined;
    });
  }

  onMount(async () => {
    if (show_code === undefined) {
      show_code = window._config.EXTRAS.indexOf("hide-code") === -1;
    }
  });
</script>

<div class="row">
  <div class="col-sm-12 col-md-9 col-lg-8 col-xl-6 p-5" style="font-family: 'Open Sans';">
    <p class="pb-3" style="font-weight: bold; font-size: 22px; color: black;">
      Multiomics2Paper: Computational Workflow to Identify Driver Pathways and Novel Targets for Cohorts of Patients
      Profiled with Transcriptomics, Proteomics, and Phosphoproteomics
    </p>
    <div class="p-2" style="border: 2px solid lightgray;">
      <p id="abstract" class="pb-2" style="font-weight: bold; font-size: 22px; color: black;">
        Abstract
      </p>
      <p class="" style="font-size: 14px; color: black;">
        In its third phase, the Clinical Proteomic Tumor Analysis Consortium (CPTAC) program collected pan-cancer data
        from 1,020 patients profiling the transcriptome, proteome, and phospho-proteome of tumors and adjacent tissues
        from ten cancer types. To identify driver cell signaling pathways and potential immunotherapeutic candidates
        from this CPTAC cohort, we applied the eXpression to Kinases (X2K) [1] and TargetRanger [2] algorithms. For each
        cancer type, tumor samples were first clustered into subtypes based on cell signaling profiles inferred from
        RNA-seq data with X2K, and then cell surface targets were prioritized for each cluster. These targets were
        subsequently confirmed for high protein expression in the tumor subtypes. For each cancer type, the
        computational pipeline identified key protein kinases and cell surface proteins that may serve as personalized
        targets. Many of these targets are also robustly differentially expressed at the proteome level. Altogether,
        this rational approach to identify key cell signaling pathways and potential targets demonstrates a pipeline
        that can be applied for personalized cancer diagnosis and therapeutic development.
      </p>
    </div>
  </div>
  <div class="col-sm-12 text-center">
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
    {#if window._config.EXTRAS.indexOf("toggle-code") !== -1}
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
    {/if}
    {#if window._config.EXTRAS.indexOf("catalog-integration") !== -1}
      <a
        id="run-notebook-locally"
        class="btn btn-primary"
        role="button"
        class:disabled={local_run_url === undefined}
        href={local_run_url}>Run Locally</a
      >
    {/if}
    <button
      type="button"
      class="btn btn-dark white"
      style="color: white !important;"
      onclick="downloadCitation()"
    >
      Export Citation
    </button>

    <div class="d-inline-block">
      <div class="dropdown">
        <button
          type="button"
          class="btn btn-dark dropdown-toggle"
          style="color: white !important;"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          Share
        </button>
        <div class="dropdown-menu">
          <div
            class="dropdown-item"
            title="Copy the link to this report"
            on:click={() => {
              navigator.clipboard.writeText(window.location.href);
            }}
          >
            Copy Link
          </div>
          <a
            class="dropdown-item"
            href={`https://www.linkedin.com/shareArticle?mini=true&url=https%3A//${window.location.host + window.location.pathname}`}
            title="Share a link to the report on LinkedIn"
            target="_blank"
            >LinkedIn</a
          >
          <a
            class="dropdown-item"
            href={`https://twitter.com/intent/tweet?text=https%3A//${window.location.host + window.location.pathname}`}
            title="Share a link to the report on X"
            target="_blank"
            >X</a
          >
        </div>
      </div>
    </div>
  </div>
  <div class="w-100">&nbsp;</div>
  {#if status}
    <div class="col-sm-8 offset-sm-2">
      <div class="alert alert-{statusBg}" role="alert">
        {status}
      </div>
    </div>
  {/if}
  <div class="w-100"></div>
  {#if $toc !== undefined}
    <Lazy
      module={() =>
        import("@/extras/catalog-integration/TableOfContents.svelte")}
      props={{ toc: $toc }}
    />
  {/if}
  {#if status === "Loading..."}
    <div class="col-sm-12 text-center">
      <Loader />
    </div>
  {/if}
  <div
    bind:this={notebookRef}
    class="col-sm-12"
    class:col-md-9={$toc !== undefined}
    class:col-xl-10={$toc !== undefined}
  >
    {#if nb}
      <Lazy
        module={() => import("@/components/jupyter/Notebook.svelte")}
        props={{
          nb,
          show_code,
          current_code_cell,
        }}
      />
    {/if}
  </div>
</div>

<style>
  /* markdown-it-anchors */
  :global(a.header-anchor) {
    text-decoration: none;
    cursor: pointer;
  }
  :global(h1) {
    display: block;
  }
  :global(h1) :global(.header-anchor) {
    display: none;
  }
  :global(h1):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h2) {
    display: block;
  }
  :global(h2) :global(.header-anchor) {
    display: none;
  }
  :global(h2):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h3) {
    display: block;
  }
  :global(h3) :global(.header-anchor) {
    display: none;
  }
  :global(h3):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h4) {
    display: block;
  }
  :global(h4) :global(.header-anchor) {
    display: none;
  }
  :global(h4):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h5) {
    display: block;
  }
  :global(h5) :global(.header-anchor) {
    display: none;
  }
  :global(h5):hover :global(.header-anchor) {
    display: inline-block;
  }
  :global(h6) {
    display: block;
  }
  :global(h6) :global(.header-anchor) {
    display: none;
  }
  :global(h6):hover :global(.header-anchor) {
    display: inline-block;
  }
  /* prompt anchors */
  :global(a.prompt-anchor) {
    text-decoration: none;
    cursor: pointer;
  }
  :global(.prompt) :global(.prompt-anchor) {
    display: inline-block;
    visibility: hidden;
  }
  :global(.prompt):hover :global(.prompt-anchor) {
    visibility: visible;
  }

  /* ensure menu appears over toc */
  .dropdown-menu {
    z-index: 1021;
  }
</style>
