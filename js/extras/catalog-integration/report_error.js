import get_require from '@/utils/get_require'

export default function report_error({ type, error }) {
  console.error(`[${type}]`, error)
  if (window._config.EXTRAS.indexOf('catalog-integration') !== -1) {
    get_require(window, 'report_error')
      .then(report_error => report_error({
        appyter: ((nb || {}).metadata || {}).appyter || null,
        url: window.location.href,
        type,
        error,
      }))
      .catch((e) => console.error('catalog-integration: failed to locate report_error handler'))
  }
}