<script>
  import auth from '@/lib/stores/keycloak_auth_store'
  import Loader from '@/components/Loader.svelte'
</script>

<div class="row">
  <div class="col-sm-12">
    <div class="mt-3 mb-0 w-100 border-custom rounded bg-lightgrey" data-toggle="collapse">
      <div class="d-table w-100 py-2 px-2 py-md-0 px-md-0">
        <div class="d-table-cell align-middle card-icon px-3 py-3 text-center">
          <i class="fas fa-cogs fa-2x" />
        </div>
        <div class="d-table-cell align-middle">
          <div class="very-small regular pb-2 pr-5">User Launch Settings</div>
          <div class="tiny light text-muted">Configure how the appyter launches</div>
        </div>
      </div>
    </div>
    <div class="border-grey mx-2 border-top-0 rounded-bottom tiny collapse show">
      {#if $auth.state === 'auth'}
        <div class="pt-3">
          <div class="row px-3 pb-3">
            <div class="col-lg-3 bold text-lg-right my-auto">
              Execution Profile:
              <sup data-toggle="tooltip" title="How the appyter should execute"><i class="far fa-question-circle"></i></sup>
            </div>
            <div class="col-lg-6 pt-2 pt-lg-0">
              <select
                name="_executor"
                class="form-control nodecoration tiny bg-white px-2 py-1 mb-0"
              >
                <option selected value="default">Execute in appyter catalog</option>
                <option value="cavatica">Execute in CAVATICA</option>
              </select>
            </div>
          </div>
          <div class="row px-4 px-lg-3 pb-4 justify-content-center">
            <div class="col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-info">
              <a href="/#/account/integrations">Click here</a> to configure additional integrations.
            </div>
          </div>
        </div>
      {:else}
        <div class="pt-3">
          <div class="row px-4 px-lg-3 pb-4 justify-content-center">
            {#if $auth.state === 'init'}
              <Loader />
            {:else if $auth.state === 'error'}
              <div class="col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-warning">
                Unable to access authentication at this time, please try again later.
              </div>
            {:else}
              <div class="col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-info">
                <button
                  type="button" class="text-btn"
                  on:click={() => $auth.keycloak.login()}
                >Login</button> to configure launch settings.
              </div>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>
