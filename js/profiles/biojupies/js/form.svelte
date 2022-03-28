<script>
  import SectionField from './fields/SectionField.svelte'
  import Loader from '@/components/Loader.svelte'
  import auth from '@/lib/stores/keycloak_auth_store'
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
          'Authorization': $auth.state === 'auth' ? `Bearer ${$auth.keycloak.token}` : null,
        },
        body: formData,
      })
      if (res.status === 406) {
        const { error: _error } = await res.json()
        error = _error
      } else {
        const { session_id } = await res.json()
        error = undefined
        window.location.href = `${window.location.href.replace(/\/$/, '')}/${session_id}/`
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
  {#if window._config.EXTRAS.indexOf('catalog-integration') !== -1 && $auth.state === 'auth'}
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
        </div>
      </div>
    </div>
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
