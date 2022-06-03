export default function ensure_string_list(v) {
  if (v === undefined || v === null) {
    return []
  } else if (typeof v === 'object' && Array.isArray(v)) {
    return v
  } else if (typeof v === 'string') {
    return v.split('\n').filter(s => s.replace(/^\s+$/, ''))
  } else {
    throw new Error('Unrecognized type')
  }
}