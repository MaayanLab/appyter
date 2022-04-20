<script>
  import auth from '@/lib/stores/keycloak_auth_store'
  import StorageFileField from '@/extras/file-field/Storage.svelte'
  import DescriptionField from '@/components/fields/DescriptionField.svelte'
  import Loader from '@/components/Loader.svelte'

  export let args
</script>

{#if $auth.state === 'auth'}
  <DescriptionField>
    <div class="text-center">
      Logged in as {$auth.keycloak.tokenParsed.email}, <button type="button" class="text-btn" on:click={() => $auth.keycloak.logout()}>click here</button> to logout.
    </div>
  </DescriptionField>
  <StorageFileField
    backend="locate"
    args={{
      ...args,
      label: 'Browse Your Uploads & Integrations',
      storage: 'user://',
    }}
  />
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
          >Login</button> to access uploads and integration storage.
        </div>
      {/if}
    </div>
  </div>
  <input
    type="text"
    style="display: none"
    name={args.name}
    value=""
  />
{/if}