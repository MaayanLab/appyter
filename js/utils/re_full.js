export default function re_full(expr, flags) {
  if (/^\^/.exec(expr) === null) expr = `^${expr}`
  if (/\$$/.exec(expr) === null) expr = `${expr}$`
  return new RegExp(expr, flags)
}