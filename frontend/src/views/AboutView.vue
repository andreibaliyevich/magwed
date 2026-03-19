<script setup>
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n({ useScope: 'global' })

useSeoMeta({
  title: () => t('seo_meta.about.title'),
  ogTitle: () => t('seo_meta.about.title'),
  description: () => t('seo_meta.about.description'),
  ogDescription: () => t('seo_meta.about.description'),
  keywords: () => t('seo_meta.about.keywords'),
  ogKeywords: () => t('seo_meta.about.keywords')
})
</script>

<template>
  <div class="about-view">
    <h1>This is an about page</h1>
  </div>
</template>
