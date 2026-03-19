<script setup>
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import PortfolioPhotoList from '@/components/auth/PortfolioPhotoList.vue'

const { t } = useI18n({ useScope: 'global' })

useHead({
  title: () => t('seo_meta.portfolio_photo_list.title')
})
</script>

<template>
  <div class="d-flex align-center my-5">
    <router-link
      :to="{ name: 'Portfolio' }"
      class="text-h4 text-md-h3 text-primary text-decoration-none"
    >
      {{ $t('portfolio.portfolio') }}
    </router-link>
    <v-icon
      icon="mdi-chevron-right"
      size="x-large"
    ></v-icon>
    <h1 class="text-h4 text-md-h3">
      {{ $t('portfolio.photos') }}
    </h1>
  </div>
  <PortfolioPhotoList />
</template>
