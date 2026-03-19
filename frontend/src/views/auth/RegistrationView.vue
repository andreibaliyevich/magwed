<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

const { t, locale } = useI18n({ useScope: 'global' })

const loadingStatus = ref(false)
const userTypeOptions = ref([])

const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const userType = ref(null)
const name = ref('')

const passwordShow = ref(false)
const password2Show = ref(false)

const status = ref(null)
const errors = ref(null)

useHead({
  title: () => t('seo_meta.registration.title')
})

const setUserTypeOptions = () => {
  userTypeOptions.value = [
    { value: 2, title: t('auth.registration.customer') },
    { value: 3, title: t('auth.registration.organizer') }
  ]
}

const registration = async () => {
  loadingStatus.value = true
  try {
    const response = await axios.post('/accounts/auth/registration/', {
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value,
      user_type: userType.value,
      name: name.value
    })
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

watch(locale, () => {
  setUserTypeOptions()
})

onMounted(() => {
  setUserTypeOptions()
})
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center mb-4">
    {{ $t('auth.registration.registration') }}
  </h1>

  <v-alert
    v-if="status === 201"
    type="success"
    variant="tonal"
  >
    {{ $t('auth.registration.success1') }}<br>
    {{ $t('auth.registration.success2') }}<br>
    {{ $t('auth.registration.success3') }}
  </v-alert>

  <div v-else>
    <p class="text-body-1 text-secondary mb-5">
      {{ $t('auth.registration.have_account') }}
      <router-link
        :to="{ name: 'Login' }"
        class="text-decoration-none"
      >
        {{ $t('auth.log_in') }}
      </router-link>
    </p>

    <v-form @submit.prevent="registration()">
      <v-text-field
        v-model="username"
        :readonly="loadingStatus"
        type="text"
        variant="filled"
        :label="$t('auth.registration.username')"
        :error-messages="errors?.username ? errors.username : []"
      ></v-text-field>
      <v-text-field
        v-model="email"
        :readonly="loadingStatus"
        type="email"
        maxlength="254"
        variant="filled"
        :label="$t('auth.registration.email')"
        :error-messages="errors?.email ? errors.email : []"
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
      <v-text-field
        v-model="password2"
        :readonly="loadingStatus"
        :type="password2Show ? 'text' : 'password'"
        variant="filled"
        :label="$t('auth.registration.password2')"
        :append-inner-icon="password2Show ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="password2Show = !password2Show"
        :error-messages="errors?.password2 ? errors.password2 : []"
      ></v-text-field>
      <v-select
        v-model="userType"
        :items="userTypeOptions"
        item-title="title"
        item-value="value"
        :readonly="loadingStatus"
        variant="filled"
        :label="$t('auth.registration.user_type')"
        :error-messages="errors?.user_type ? errors.user_type : []"
      ></v-select>
      <v-text-field
        v-model="name"
        :readonly="loadingStatus"
        type="text"
        variant="filled"
        :label="$t('auth.registration.name')"
        :error-messages="errors?.name ? errors.name : []"
      ></v-text-field>
      <v-btn
        :loading="loadingStatus"
        type="submit"
        variant="flat"
        color="primary"
        size="x-large"
        block
      >
        {{ $t('auth.register') }}
      </v-btn>
    </v-form>

    <v-divider class="my-3"></v-divider>
    <p class="text-body-1 text-secondary">
      {{ $t('auth.registration.help') }}
    </p>
  </div>
</template>
