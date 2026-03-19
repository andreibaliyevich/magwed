import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, computed, watch } from 'vue'

export function useOptionsOfCities(country) {
  const { t } = useI18n({ useScope: 'global' })
  const cityValues = ref([])

  const cityOptions = computed(() => {
    return cityValues.value.map((element) => {
      return {
        value: element.code,
        title: t(`cities.${element.code}`)
      }
    })
  })

  const getAndSetCityOptions = async (countryValue) => {
    try {
      const response = await axios.get('/main/cities/', {
        params: {
          country: countryValue
        }
      })
      cityValues.value = response.data
    } catch (error) {
      console.error(error)
    }
  }

  watch(country, async (newValue) => {
    if (newValue) {
      await getAndSetCityOptions(newValue)
    } else {
      cityValues.value = []
    }
  })

  return { cityOptions }
}
