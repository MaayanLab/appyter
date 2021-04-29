export default function ensure_list(L) {
  if (typeof L === 'object' && Array.isArray(L)) {
    return L
  } else {
    return [L]
  }
}