export default async function get_require(window, required) {
  let ret
  if (Array.isArray(required)) {
    ret = new Promise((resolve, reject) => window.require(required, (...args) => resolve(args), reject))
  } else {
    ret = new Promise((resolve, reject) => window.require([required], resolve, reject))
  }
  while (ret instanceof Promise) ret = await ret
  return ret
}
