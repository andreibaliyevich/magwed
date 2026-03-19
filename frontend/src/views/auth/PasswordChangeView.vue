<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

const { t } = useI18n({ useScope: 'global' })

const passwordUpdating = ref(false)

const currentPassword = ref('')
const newPassword = ref('')
const newPassword2 = ref('')

const currentPasswordShow = ref(false)
const newPasswordShow = ref(false)
const newPassword2Show = ref(false)

const status = ref(null)
const errors = ref(null)

useHead({
  title: () => t('seo_meta.password_change.title')
})

const changePassword = async () => {
  passwordUpdating.value = true
  try {
    const response = await axios.post('/accounts/auth/password/change/', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
      new_password2: newPassword2.value
    })
    currentPassword.value = ''
    newPassword.value = ''
    newPassword2.value = ''
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    passwordUpdating.value = false
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
  }
}
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center my-5">
    {{ $t('auth.passwordchange.password_change') }}
  </h1>

  <v-alert
    v-if="status === 204"
    type="success"
    variant="tonal"
    closable
  >
    {{ $t('auth.passwordchange.success') }}
  </v-alert>

  <v-list class="text-body-1">
    <v-list-item prepend-icon="mdi-circle-small">
      {{ $t('auth.password.advice1') }}
    </v-list-item>
    <v-list-item prepend-icon="mdi-circle-small">
      {{ $t('auth.password.advice2') }}
    </v-list-item>
    <v-list-item prepend-icon="mdi-circle-small">
      {{ $t('auth.password.advice3') }}
    </v-list-item>
    <v-list-item prepend-icon="mdi-circle-small">
      {{ $t('auth.password.advice4') }}
    </v-list-item>
  </v-list>

  <v-form
    @submit.prevent="changePassword()"
    class="mb-10"
  >
    <v-text-field
      v-model="currentPassword"
      :readonly="passwordUpdating"
      :type="currentPasswordShow ? 'text' : 'password'"
      variant="filled"
      :label="$t('auth.passwordchange.current_password')"
      :append-inner-icon="currentPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append-inner="currentPasswordShow = !currentPasswordShow"
      :error-messages="errors?.current_password ? errors.current_password : []"
    ></v-text-field>
    <v-text-field
      v-model="newPassword"
      :readonly="passwordUpdating"
      :type="newPasswordShow ? 'text' : 'password'"
      variant="filled"
      :label="$t('auth.password.new_password')"
      :append-inner-icon="newPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append-inner="newPasswordShow = !newPasswordShow"
      :error-messages="errors?.new_password ? errors.new_password : []"
    ></v-text-field>
    <v-text-field
      v-model="newPassword2"
      :readonly="passwordUpdating"
      :type="newPassword2Show ? 'text' : 'password'"
      variant="filled"
      :label="$t('auth.password.new_password2')"
      :append-inner-icon="newPassword2Show ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append-inner="newPassword2Show = !newPassword2Show"
      :error-messages="errors?.new_password2 ? errors.new_password2 : []"
    ></v-text-field>
    <v-btn
      :loading="passwordUpdating"
      type="submit"
      variant="flat"
      color="primary"
      size="x-large"
      class="text-none mt-3"
    >
      {{ $t('auth.passwordchange.change_password') }}
    </v-btn>
  </v-form>
</template>
