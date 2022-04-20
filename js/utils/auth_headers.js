export default async function auth_headers(auth) {
  let token
  if (auth.state === 'auth') {
    token = await auth.keycloak.getValidToken()
  }
  if (token !== undefined && token !== null) {
    return { 'Authorization': `Bearer ${token}` }
  } else {
    return {}
  }
}