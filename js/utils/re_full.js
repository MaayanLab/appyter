export default function re_full(expr) {
  if (/^\^/.exec(expr) === null) expr = `^${expr}`
  if (/\$$/.exec(expr) === null) expr = `${expr}$`
  return new RegExp(expr)
}