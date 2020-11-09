export default function collapse(text, join='') {
  if (Array.isArray(text)) {
    return text.join(join)
  } else {
    return text
  }
}