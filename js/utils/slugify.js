export default function slugify(l) {
  return l
    .toLowerCase()
    .replace(/[^A-Za-z0-9_-]/g, '-')
    .replace(/^-+/g, '')
    .replace(/-+$/g, '')
}
