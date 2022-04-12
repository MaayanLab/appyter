<script>
  import SectionField from './fields/SectionField.svelte'
  import Loader from '@/components/Loader.svelte'
  import auth from '@/lib/stores/keycloak_auth_store'
  import Lazy from '@/components/Lazy.svelte'
  import url_for from '@/utils/url_for'
  import auth_headers from '@/utils/auth_headers'
  export let fields = []

  let submitting = false
  let error
  let orphaned_fields
  $: orphaned_fields = fields.filter(field => field.type !== 'section' && !field.args.section)

  function with_error(field, error) {
    if (error !== undefined && error.cls === 'FieldConstraintException') {
      if (field.args.name === error.field_name) {
        field.error = error
      }
    }
    return field
  }

  async function onSubmit(evt) {
    try {
      submitting = true
      const formData = new FormData(evt.target)
      const res = await fetch(window.location.href, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          ...(await auth_headers($auth)),
        },
        body: formData,
      })
      if (res.status === 406) {
        const { error: _error } = await res.json()
        error = _error
      } else {
        const { _id, _storage, _executor } = await res.json()
        error = undefined
        window.location.href = url_for({ path: `${window._config.ORIGIN}/${_id}/`, params: { storage: _storage, executor: _executor } })
      }
    } catch (e) {
      error = { cls: 'FrontendException', message: e.toString() }
    } finally {
      submitting = false
    }
  }
  $: if (error) {
    console.error(error)
  }
</script>

<form
  method="POST"
  enctype="multipart/form-data"
  action="#"
  on:submit|preventDefault={onSubmit}
>
  {#if orphaned_fields.length > 0}
    <SectionField
      args={{
        name: '_primary',
        section: null,
        title: 'Appyter',
        subtitle: 'Customize your notebook',
        icon: 'cogs',
      }}
      fields={orphaned_fields.map(field => with_error(field, error))}
    />
  {/if}
  {#each fields.filter(field => field.type === 'section') as field}
    {#if field.field === 'SectionField'}
      <SectionField
        args={field.args}
        fields={fields.filter(_field => _field.args.section === field.args.name).map(field => with_error(field, error))}
      />
    {/if}
  {/each}
  {#if window._config.EXTRAS.indexOf('catalog-integration') !== -1}
    <Lazy
      module={() => import('@/extras/catalog-integration/LaunchSettings.svelte')}
    />
  {/if}
  <div class="row">
    <div class="col-sm-12">
      &nbsp;
    </div>
    {#if error !== undefined && error.cls !== 'FieldConstraintException'}
    <div class="col-sm-12 alert alert-danger">
      {error.message}
    </div>
    {/if}
    <div class="col-sm-12 text-center">
      {#if submitting}
        <Loader />
      {:else}
        <input
          class="btn navigate white border-custom bg-blue nodecoration"
          type="submit"
          value="Submit"
        />
      {/if}
    </div>
  </div>
</form>
