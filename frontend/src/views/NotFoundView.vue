<script setup>
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import NotFound from '@/components/NotFound.vue'

const { t } = useI18n({ useScope: 'global' })

useHead({
  title: () => t('seo_meta.not_found.title')
})
</script>

<template>
  <div class="not-found-view">
    <NotFound />
  </div>
</template>
