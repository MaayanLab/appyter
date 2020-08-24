export default function any(L) {
  for (const el of L) {
    if (el) return true
  }
  return false
}