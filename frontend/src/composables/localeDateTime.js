import { useI18n } from 'vue-i18n'

export function useLocaleDateTime() {
  const { locale } = useI18n({ useScope: 'global' })

  const getLocaleDateString = (dateTimeString) => {
    const dateTime = new Date(dateTimeString)
    return dateTime.toLocaleDateString(locale.value, {
      dateStyle: 'medium'
    })
  }

  const getLocaleDateTimeString = (dateTimeString) => {
    const dateTime = new Date(dateTimeString)
    return dateTime.toLocaleTimeString(locale.value, {
      timeStyle: 'short'
    }) + " | " + dateTime.toLocaleDateString(locale.value, {
      dateStyle: 'medium'
    })
  }

  return {
    getLocaleDateString,
    getLocaleDateTimeString
  }
}
