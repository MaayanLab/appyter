<script>
  import auth from '@/lib/stores/keycloak_auth_store'
  import Loader from '@/components/Loader.svelte'
  import SectionField from '@/components/fields/SectionField.svelte'
  import DescriptionField from '@/components/fields/DescriptionField.svelte'
  import TabField from '@/components/fields/TabField.svelte'
  import StringField from '@/components/fields/StringField.svelte'
  import auth_headers from '@/utils/auth_headers'

  const executor_map = {
    'default': 'Our Cloud',
    'cavatica': 'CAVATICA',
  }

  const executor_hints = (window._config.HINTS || [])
    .reduce((executor_hints, hint) => {
      const m = /^executor:(.+)$/.exec(hint)
      if (m !== null) return [...executor_hints, m[1]]
      else return executor_hints
    }, [])

  const choices = executor_hints.length > 0 ?
    executor_hints.reduce(
      (executors, executor) =>
        executor in executor_map ?
          [...executors, executor_map[executor]]
          : executors,
      [],
    )
    : Object.values(executor_map)

  let config
  async function get_config() {
    const res = await fetch(`${window._config.CATALOG_ORIGIN}/postgrest/rpc/user_config`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(await auth_headers($auth)),
      },
      body: JSON.stringify({ config: null })
    })
    if (res.status === 200) {
      return await res.json()
    } else {
      console.error(await res.text())
    }
  }

  $: if ($auth.state === 'auth') {
    get_config()
      .then(c => config = c)
      .catch(e => console.error(e))
  }
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
        Logged in as {$auth.keycloak.tokenParsed.email}, <a href="{window._config.CATALOG_ORIGIN}/#/account/">click here</a> to manage your account.
      </div>
    </DescriptionField>
    <TabField
      args={{
        name: '_executor',
        label: 'Execution Profile',
        description: 'How the appyter should be executed',
        value: choices[0],
        choices,
      }}
      let:tab={tab}
    >
      {#if tab === executor_map['default']}
        <input
          type="text"
          class="hidden"
          name="_executor"
          value=""
        />
        <DescriptionField>
          <span style="font-weight: 600">Execute using Public Appyter Catalog Resources</span>
        </DescriptionField>
      {:else if tab === executor_map['cavatica']}
        <input
          type="text"
          class="hidden"
          name="_executor"
          value="cavatica"
        />
        {#if config !== undefined}
          {#if !config.cavatica_api_key}
            <DescriptionField>
              <div class="alert alert-warning">CAVATICA Integration is not configured, please <a href="{window._config.CATALOG_ORIGIN}/#/account/integrations/cavatica">click here to learn more</a>.</div>
            </DescriptionField>
          {:else}
            <DescriptionField>
              <span style="font-weight: 600">Execute in CAVATICA</span>
            </DescriptionField>
            <StringField
              args={{
                value: config.cavatica_project || '',
                name: '_cavatica_project',
                label: 'CAVATICA Project',
                constraint: '^[^/]+/[^/]+$',
                feedback: 'String is invalid, should be of the form: cavatica-username/cavatica-project',
              }}
            />
          {/if}
        {:else}
          <Loader />
        {/if}
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
