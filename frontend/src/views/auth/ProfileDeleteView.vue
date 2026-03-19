<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useUserStore } from '@/stores/user.js'

const router = useRouter()
const { t, locale } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const profileDeleting = ref(false)
const currentPassword = ref('')
const currentPasswordShow = ref(false)

const errors = ref(null)

useHead({
  title: () => t('seo_meta.profile_delete.title')
})

const deletingProfile = async () => {
  profileDeleting.value = true
  try {
    const response = await axios.delete('/accounts/auth/profile/', {
      data: {
        current_password: currentPassword.value
      }
    })
    errors.value = null
    window.localStorage.removeItem('user')
    userStore.$reset()
    router.push({
      name: 'Home',
      params: { locale: locale.value }
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    profileDeleting.value = false
  }
}
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center my-5">
    {{ $t('auth.profile_delete.profile_delete') }}
  </h1>

  <p class="text-body-1 mb-5">
    {{ $t('auth.profile_delete.advice1') }}<br>
    {{ $t('auth.profile_delete.advice2') }}
  </p>

  <v-form
    @submit.prevent="deletingProfile()"
    class="mb-10"
  >
    <v-text-field
      v-model="currentPassword"
      :readonly="profileDeleting"
      :type="currentPasswordShow ? 'text' : 'password'"
      variant="filled"
      :label="$t('auth.profile_delete.password_confirmation')"
      :append-inner-icon="currentPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append-inner="currentPasswordShow = !currentPasswordShow"
      :error-messages="errors?.current_password ? errors.current_password : []"
    ></v-text-field>
    <v-btn
      :loading="profileDeleting"
      type="submit"
      variant="flat"
      color="primary"
      size="x-large"
      class="text-none mt-3"
    >
      {{ $t('auth.profile_delete.delete_profile') }}
    </v-btn>
  </v-form>
</template>
