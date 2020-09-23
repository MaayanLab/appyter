import canonicalJson from 'canonical-json/index2.js'

export default function hashObject(obj) {
  return canonicalJson(obj)
}
