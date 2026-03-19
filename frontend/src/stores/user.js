import { defineStore } from 'pinia'

export const useUserStore = defineStore('userStore', {
  state: () => ({
    uuid: null,
    username: null,
    email: null,
    userType: null,
    name: null,
    avatar: null,
    token: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    setUserData(data) {
      this.$patch({
        uuid: data.uuid,
        username: data.username,
        email: data.email,
        userType: data.user_type,
        name: data.name,
        avatar: data.avatar,
        token: data.token
      })
    },
    updateUsername(value) {
      this.username = value
    },
    updateEmail(value) {
      this.email = value
    },
    updateName(value) {
      this.name = value
    },
    updateAvatar(value) {
      this.avatar = value
    }
  }
})
