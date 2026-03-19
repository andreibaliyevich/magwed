import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export function useOptionsOfCountries() {
  const { t } = useI18n({ useScope: 'global' })

  const countryOptions = computed(() => {
    return [
      { value: 'BY', title: t('countries.BY') },
      { value: 'RU', title: t('countries.RU') },
      { value: 'UA', title: t('countries.UA') }
    ]
  })

  return { countryOptions }
}
