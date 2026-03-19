import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export function useOptionsOfRoleTypes(translationKey) {
  const { t } = useI18n({ useScope: 'global' })

  const roleTypeOptions = computed(() => {
    return [
      { value: 1, title: t(`${translationKey}.1`) },
      { value: 2, title: t(`${translationKey}.2`) },
      { value: 3, title: t(`${translationKey}.3`) },
      { value: 4, title: t(`${translationKey}.4`) },
      { value: 5, title: t(`${translationKey}.5`) },
      { value: 6, title: t(`${translationKey}.6`) },
      { value: 7, title: t(`${translationKey}.7`) },
      { value: 8, title: t(`${translationKey}.8`) },
      { value: 9, title: t(`${translationKey}.9`) },
      { value: 10, title: t(`${translationKey}.10`) },
      { value: 11, title: t(`${translationKey}.11`) }
    ]
  })

  return { roleTypeOptions }
}
