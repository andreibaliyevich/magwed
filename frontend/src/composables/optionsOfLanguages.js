import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export function useOptionsOfLanguages() {
  const { t } = useI18n({ useScope: 'global' })

  const languageOptions = computed(() => {
    return [
      { value: 'be', title: t('languages.be') },
      { value: 'en', title: t('languages.en') },
      { value: 'fr', title: t('languages.fr') },
      { value: 'de', title: t('languages.de') },
      { value: 'pl', title: t('languages.pl') },
      { value: 'pt', title: t('languages.pt') },
      { value: 'ru', title: t('languages.ru') },
      { value: 'uk', title: t('languages.uk') }
    ]
  })

  return { languageOptions }
}
