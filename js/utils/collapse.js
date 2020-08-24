export default function collapse(text) {
  if (Array.isArray(text)) {
    return text.join('')
  } else {
    return text
  }
}