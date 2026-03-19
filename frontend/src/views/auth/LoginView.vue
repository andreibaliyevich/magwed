<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()
const { t, locale } = useI18n({ useScope: 'global' })

const loadingStatus = ref(false)
const username = ref('')
const password = ref('')
const passwordShow = ref(false)

const errors = ref(null)

useHead({
  title: () => t('seo_meta.login.title')
})

const login = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post('/accounts/auth/login/', {
      username: username.value,
      password: password.value
    })
    window.localStorage.setItem('user', JSON.stringify(response.data))
    if (route.query.redirect) {
      window.location.assign(`${route.query.redirect}`)
    } else {
      window.location.assign(`/${locale.value}`)
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
  }
}
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center mb-4">
    {{ $t('auth.login.login') }}
  </h1>

  <div v-if="errors && errors.non_field_errors">
    <v-alert
      type="error"
      variant="tonal"
    >
      <div
        v-for="error in errors.non_field_errors"
        class="ms-3"
      >
        {{ error }}
      </div>
    </v-alert>
  </div>

  <p class="text-grey-darken-2 mb-5">
    {{ $t('auth.login.have_account') }}
    <router-link
      :to="{ name: 'Registration' }"
      class="text-decoration-none"
    >
      {{ $t('auth.register') }}
    </router-link>
  </p>
  <v-form @submit.prevent="login()">
    <v-text-field
      v-model="username"
      :readonly="loadingStatus"
      type="text"
      variant="filled"
      :label="$t('auth.login.username_email')"
      :error-messages="errors?.username ? errors.username : []"
    ></v-text-field>
    <v-text-field
      v-model="password"
      :readonly="loadingStatus"
      :type="passwordShow ? 'text' : 'password'"
      variant="filled"
      :label="$t('auth.password.password')"
      :append-inner-icon="passwordShow ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append-inner="passwordShow = !passwordShow"
      :error-messages="errors?.password ? errors.password : []"
    ></v-text-field>
    <v-btn
      :loading="loadingStatus"
      type="submit"
      variant="flat"
      color="primary"
      size="x-large"
      block
    >
      {{ $t('auth.log_in') }}
    </v-btn>
  </v-form>
  <v-divider class="my-5"></v-divider>
  <p class="text-grey-darken-2">
    {{ $t('auth.login.forgot_your_password') }}
    <router-link
      :to="{ name: 'PasswordReset' }"
      class="text-decoration-none"
    >
      {{ $t('auth.password.reset_password') }}
    </router-link>
  </p>
</template>
