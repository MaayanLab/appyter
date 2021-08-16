export default function get_require(window, required) {
  if (Array.isArray(required)) {
    return new Promise((resolve, reject) => window.require(required, (...args) => resolve(args), reject))
  } else {
    return new Promise((resolve, reject) => window.require([required], resolve, reject))
  }
}
