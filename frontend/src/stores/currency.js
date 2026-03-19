import axios from 'axios'
import { defineStore } from 'pinia'
import { CURRENCIES } from '@/config.js'

export const useCurrencyStore = defineStore('currencyStore', {
  state: () => ({
    currencyValue: CURRENCIES[0].value,
    currencySymbol: CURRENCIES[0].symbol,
    conversionRate: 1
  }),
  actions: {
    async setCurrency(value) {
      this.currencyValue = value

      CURRENCIES.forEach((element) => {
        if (element.value === value) {
          this.currencySymbol = element.symbol
        }
      })

      try {
        const response = await axios.get(
          '/main/currencies/'
            + value
            + '/'
        )
        this.conversionRate = response.data.conversion_rate
      } catch (error) {
        console.error(error)
      }
    },
    convertCurrency(value) {
      return (value * this.conversionRate).toFixed(2)
    }
  }
})
