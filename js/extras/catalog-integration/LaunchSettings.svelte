<script>
  import auth from '@/lib/stores/keycloak_auth_store'
  import Loader from '@/components/Loader.svelte'
  import SectionField from '@/components/fields/SectionField.svelte'
  import DescriptionField from '@/components/fields/DescriptionField.svelte'
  import TabField from '@/components/fields/TabField.svelte'
  import StringField from '@/components/fields/StringField.svelte'
</script>

<SectionField
  args={{
    name: '_user_launch',
    title: 'User Launch Settings',
    subtitle: 'Configure how the appyter launches',
    icon: 'cogs',
  }}
>
  {#if $auth.state === 'auth'}
    <DescriptionField>
      <div class="text-center">
        Logged in as {$auth.keycloak.tokenParsed.email}, <button type="button" class="text-btn" on:click={() => $auth.keycloak.logout()}>click here</button> to logout.
      </div>
    </DescriptionField>
    <TabField
      args={{
        name: '_executor',
        label: 'Execution Profile',
        description: 'How the appyter should be executed',
        value: 'Catalog',
        choices: ['Catalog', 'CAVATICA'],
      }}
      let:tab={tab}
    >
      {#if tab === 'Catalog'}
        <DescriptionField>
          <span style="font-weight: 600">Execute using Public Appyter Catalog Resources</span>
        </DescriptionField>
      {:else if tab === 'CAVATICA'}
        <DescriptionField>
          <span style="font-weight: 600">Execute in CAVATICA</span>: For more information, or to configure CAVATICA integration, <a href="/#/account/integrations/cavatica">click here</a>.
        </DescriptionField>
        <StringField
          args={{
            name: 'cavatica_project',
            label: 'CAVATICA Project',
          }}
        />
      {/if}
    </TabField>
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
</SectionField>
