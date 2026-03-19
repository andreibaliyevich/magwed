import axios from 'axios'
import { useI18n } from 'vue-i18n'

export function useLogout() {
  const { locale } = useI18n({ useScope: 'global' })

  const logout = () => {
    axios.post('/accounts/auth/logout/')
    .then(() => {
      window.localStorage.removeItem('user')
      window.location.assign(`/${locale.value}`)
    })
  }

  return { logout }
}
