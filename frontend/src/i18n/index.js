import axios from 'axios'
import { createI18n } from 'vue-i18n'
import { nextTick } from 'vue'
import { API_URL, LANGUAGES } from '@/config.js'
import { pluralSlavicRule } from './rules.js'

export const SUPPORT_LOCALES = Array.from(LANGUAGES, element => element.value)

function getStartingLocale() {
  const navigatorLocale = window.navigator.language.split('-')[0]

  if (SUPPORT_LOCALES.includes(navigatorLocale)) {
    return navigatorLocale
  }

  return SUPPORT_LOCALES[0]
}

export async function loadLocaleMessages(i18n, locale) {
  const messages = await import(`./locales/${locale}.json`)
  i18n.global.setLocaleMessage(locale, messages.default)
  return nextTick()
}

export function setI18nLanguage(i18n, locale) {
  i18n.global.locale.value = locale
  axios.defaults.baseURL = `${API_URL}/${locale}`
  axios.defaults.headers.common['Accept-Language'] = locale
  document.querySelector('html').setAttribute('lang', locale)
}

const startingLocale = getStartingLocale()

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: startingLocale,
  fallbackLocale: 'en',
  pluralRules: {
    ru: pluralSlavicRule,
    be: pluralSlavicRule,
    uk: pluralSlavicRule
  }
})
await loadLocaleMessages(i18n, startingLocale)
setI18nLanguage(i18n, startingLocale)

export default i18n
