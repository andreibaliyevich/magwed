<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { ref, onMounted } from 'vue'
import { WS_URL } from '@/config.js'
import { useCurrencyStore } from '@/stores/currency.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import Header from '@/components/main/Header.vue'
import Footer from '@/components/main/Footer.vue'
import ScrollTopButton from '@/components/main/ScrollTopButton.vue'

useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} | MAGWED` : 'MAGWED';
  }
})

const currencyStore = useCurrencyStore()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const deviceUUID = ref(null)
const connectionSocket = ref(null)

axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response.status === 401) {
      window.localStorage.removeItem('user')
      window.location.reload()
    }
    return Promise.reject(error)
  }
)

deviceUUID.value = window.localStorage.getItem('deviceUUID')
if (!deviceUUID.value) {
  deviceUUID.value = crypto.randomUUID()
  window.localStorage.setItem('deviceUUID', deviceUUID.value)
}

const currency = window.localStorage.getItem('currency')
if (currency) {
  currencyStore.setCurrency(currency)
}

const userString = window.localStorage.getItem('user')
if (userString) {
  const userData = JSON.parse(userString)
  axios.defaults.headers.common['Authorization'] = `Token ${userData.token}`
  userStore.setUserData(userData)
}

onMounted(() => {
  let connectionSocketURL = `${WS_URL}/ws/connection/${deviceUUID.value}/`
  if (userStore.isLoggedIn) {
    connectionSocketURL += `?${userStore.token}`
  }
  connectionSocket.value = new WebSocket(connectionSocketURL)
  connectionSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.user_uuid === userStore.uuid && data.status !== 'online') {
      connectionSocket.value.send(JSON.stringify({'status': 'online'}))
    } else {
      connectionBusStore.setUserStatus(data)
    }
  }
})
</script>

<template>
  <v-app>
    <Header />
    <v-main>
      <router-view />
    </v-main>
    <Footer />
    <ScrollTopButton />
  </v-app>
</template>

<style>
@import '@/assets/base.css';
</style>
