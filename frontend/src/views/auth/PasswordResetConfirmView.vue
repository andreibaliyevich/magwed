<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()
const { t } = useI18n({ useScope: 'global' })

const loadingStatus = ref(false)

const newPassword = ref('')
const newPassword2 = ref('')

const newPasswordShow = ref(false)
const newPassword2Show = ref(false)

const status = ref(null)
const errors = ref(null)

useHead({
  title: () => t('seo_meta.password_reset_confirm.title')
})

const confirmPasswordReset = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post(
      '/accounts/auth/password/reset/confirm/',
      {
        uid: route.params.uid,
        token: route.params.token,
        new_password: newPassword.value,
        new_password2: newPassword2.value
      }
    )
    newPassword.value = ''
    newPassword2.value = ''
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
  }
}
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center mb-4">
    {{ $t('auth.passwordresetconfirm.password_reset_confirm') }}
  </h1>

  <v-alert
    v-if="status === 204"
    type="success"
    variant="tonal"
    :title="$t('auth.passwordresetconfirm.success1')"
  >
    <p class="text-body-1 text-secondary">
      {{ $t('auth.passwordresetconfirm.success2') }}<br>
      {{ $t('auth.passwordresetconfirm.success3') }}
    </p>
    <div class="text-center mt-3">
      <router-link
        :to="{ name: 'Login' }"
        class="text-decoration-none"
      >
        {{ $t('auth.log_in') }}
      </router-link>
    </div>
  </v-alert>

  <v-alert
    v-else-if="errors && (errors.detail || errors.non_field_errors || errors.uid || errors.token)"
    type="error"
    variant="tonal"
    :title="$t('auth.passwordresetconfirm.error')"
  >
    <p
      v-if="errors.detail"
      class="text-body-1 text-secondary"
    >
      {{ errors.detail }}
    </p>
    <p
      v-if="errors.non_field_errors"
      class="text-body-1 text-secondary"
    >
      <div v-for="error in errors.non_field_errors">
        {{ error }}<br>
      </div>
    </p>
    <p
      v-if="errors.uid"
      class="text-body-1 text-secondary"
    >
      <div v-for="error in errors.uid">
        {{ error }}<br>
      </div>
    </p>
    <p
      v-if="errors.token"
      class="text-body-1 text-secondary"
    >
      <div v-for="error in errors.token">
        {{ error }}<br>
      </div>
    </p>
    <div class="text-center mt-3">
      <router-link
        :to="{ name: 'PasswordReset' }"
        class="text-decoration-none"
      >
        {{ $t('auth.password.reset_password') }}
      </router-link>
    </div>
  </v-alert>

  <div v-else>
    <v-list class="text-body-1 text-secondary">
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

    <v-form @submit.prevent="confirmPasswordReset()">
      <v-text-field
        v-model="newPassword"
        :readonly="loadingStatus"
        :type="newPasswordShow ? 'text' : 'password'"
        variant="filled"
        :label="$t('auth.password.new_password')"
        :append-inner-icon="newPasswordShow ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="newPasswordShow = !newPasswordShow"
        :error-messages="errors?.new_password ? errors.new_password : []"
      ></v-text-field>
      <v-text-field
        v-model="newPassword2"
        :readonly="loadingStatus"
        :type="newPassword2Show ? 'text' : 'password'"
        variant="filled"
        :label="$t('auth.password.new_password2')"
        :append-inner-icon="newPassword2Show ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="newPassword2Show = !newPassword2Show"
        :error-messages="errors?.new_password2 ? errors.new_password2 : []"
      ></v-text-field>
      <v-btn
        :loading="loadingStatus"
        type="submit"
        variant="flat"
        color="primary"
        size="x-large"
        block
      >
        {{ $t('auth.passwordresetconfirm.confirm_password_reset') }}
      </v-btn>
    </v-form>
  </div>
</template>
