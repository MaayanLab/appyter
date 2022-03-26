import get_require from '@/utils/get_require'

export default function pagehit(pagehit_type) {
  if (window._config.EXTRAS.indexOf('catalog-integration') !== -1) {
    get_require(window, 'pagehit')
      .then(catalog_pagehit => catalog_pagehit(pagehit_type))
      .catch(e => {
        console.error('catalog-integration: pagehit error')
        console.error(e)
      })
  }
}