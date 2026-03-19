import { defineStore } from 'pinia'

export const useConnectionBusStore = defineStore('connectionBusStore', {
  state: () => ({
    user_uuid: null,
    status: null
  }),
  actions: {
    setUserStatus(data) {
      this.$patch({
        user_uuid: data.user_uuid,
        status: data.status
      })
    }
  }
})
