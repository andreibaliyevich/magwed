<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'

const route = useRoute()
const { t } = useI18n({ useScope: 'global' })

const loadingStatus = ref(true)

const status = ref(null)
const errors = ref(null)

useHead({
  title: () => t('seo_meta.activation.title')
})

onMounted(async () => {
  try {
    const response = await axios.post('/accounts/auth/activation/', {
      uid: route.params.uid,
      token: route.params.token
    })
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
  }
})
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center mb-4">
    {{ $t('auth.activation.activation') }}
  </h1>

  <div
    v-if="loadingStatus"
    class="d-flex justify-center align-center my-15"
  >
    <v-progress-circular
      indeterminate
      :size="80"
    ></v-progress-circular>
  </div>

  <v-alert
    v-else-if="status === 204"
    type="success"
    variant="tonal"
    :title="$t('auth.activation.success1')"
  >
    <p class="text-body-1 text-secondary">
      {{ $t('auth.activation.success2') }}<br>
      {{ $t('auth.activation.success3') }}
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
    v-else-if="errors"
    type="error"
    variant="tonal"
    :title="$t('auth.activation.error')"
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
        :to="{ name: 'Registration' }"
        class="text-decoration-none"
      >
        {{ $t('auth.register') }}
      </router-link>
    </div>
  </v-alert>
</template>
