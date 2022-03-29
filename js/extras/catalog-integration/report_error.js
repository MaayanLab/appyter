import get_require from '@/utils/get_require'

export default function report_error({ type, error }) {
  console.error(`[${type}]`, error)
  if (window._config.EXTRAS.indexOf('catalog-integration') !== -1) {
    if (window._config.report_error !== undefined) {
      window._config.report_error({ type, error })
    } else {
      console.warn('[catalog-integration:report_error]: attempting deprecated requirejs resolution')
      get_require(window, 'report_error')
        .then(report_error => {
          console.warn('[catalog-integration:report_error]: deprecated report_error')
          report_error({
            appyter: ((nb || {}).metadata || {}).appyter || null,
            url: window.location.href,
            type,
            error,
          })
        })
        .catch((e) => {})
    }
  }
}
