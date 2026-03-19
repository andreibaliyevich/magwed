<script setup>
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n({ useScope: 'global' })

useSeoMeta({
  title: () => t('seo_meta.home.title'),
  ogTitle: () => t('seo_meta.home.title'),
  description: () => t('seo_meta.home.description'),
  ogDescription: () => t('seo_meta.home.description'),
  keywords: () => t('seo_meta.home.keywords'),
  ogKeywords: () => t('seo_meta.home.keywords')
})
</script>

<template>
  <div class="home-view">
    <h1>This is a hone page</h1>
  </div>
</template>
