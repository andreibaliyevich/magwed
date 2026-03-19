<script setup>
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { userType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import ProfileAvatar from '@/components/auth/ProfileAvatar.vue'
import ProfileCover from '@/components/auth/ProfileCover.vue'
import AdminProfileForm from '@/components/auth/AdminProfileForm.vue'
import CustomerProfileForm from '@/components/auth/CustomerProfileForm.vue'
import OrganizerProfileForm from '@/components/auth/OrganizerProfileForm.vue'

const { t } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

useHead({
  title: () => t('seo_meta.profile.title')
})
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center my-5">
    {{ $t('user.profile_settings') }}
  </h1>

  <ProfileCover v-if="userStore.userType === userType.ORGANIZER" />
  <ProfileAvatar />

  <AdminProfileForm v-if="userStore.userType === userType.ADMIN" />
  <CustomerProfileForm v-else-if="userStore.userType === userType.CUSTOMER" />
  <OrganizerProfileForm v-else-if="userStore.userType === userType.ORGANIZER" />
</template>
