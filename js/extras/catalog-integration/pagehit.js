import get_require from '@/utils/get_require'

export default function pagehit(pagehit_type) {
  if (window._config.EXTRAS.indexOf('catalog-integration') !== -1) {
    if (window._config.pagehit !== undefined) {
      window._config.pagehit(pagehit_type)
    } else {
      console.info(`[catalog-integration:pagehit]: ${pagehit_type}`)
      console.warn('[catalog-integration:pagehit]: attempting deprecated requirejs resolution')
      get_require(window, 'pagehit')
        .then(catalog_pagehit => {
          console.warn('[catalog-integration:pagehit]: deprecated requirejs pagehit')
          catalog_pagehit(pagehit_type)
        })
        .catch(e => {})
    }
  }
}
