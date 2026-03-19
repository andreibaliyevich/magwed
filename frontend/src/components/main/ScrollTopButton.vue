<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isActive = ref(false)

const handleScroll = () => {
  isActive.value = window.scrollY > 500
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <v-fab
    :active="isActive"
    @click="scrollToTop"
    :transition="isActive ? 'scroll-y-reverse-transition' : 'scroll-y-transition'"
    icon="mdi-chevron-up"
    color="primary"
    variant="tonal"
    app
    location="bottom end"
  ></v-fab>
</template>
