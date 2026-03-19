<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCities } from '@/composables/optionsOfCities.js'

const userStore = useUserStore()

const profileLoading = ref(true)
const profileUpdating = ref(false)

const name = ref('')
const country = ref(null)
const city = ref(null)
const phone = ref('')
const dateOfWedding = ref(null)

const { countryOptions } = useOptionsOfCountries()
const { cityOptions } = useOptionsOfCities(country)

const errors = ref(null)

const getProfileData = async () => {
  try {
    const response = await axios.get('/accounts/auth/profile/')
    name.value = response.data.user.name
    country.value = response.data.user.country
    city.value = response.data.user.city
    phone.value = response.data.user.phone
    dateOfWedding.value = response.data.date_of_wedding
  } catch (error) {
    console.error(error)
  } finally {
    profileLoading.value = false
  }
}

const updateProfile = async () => {
  profileUpdating.value = true

  if (!country.value) {
    country.value = null
  }
  if (!city.value) {
    city.value = null
  }
  if (!dateOfWedding.value) {
    dateOfWedding.value = null
  }

  try {
    const response = await axios.put('/accounts/auth/profile/', {
      user: {
        name: name.value,
        country: country.value,
        city: city.value,
        phone: phone.value
      },
      date_of_wedding: dateOfWedding.value
    })
    if (response.status === 204) {
      userStore.updateName(name.value)
      window.localStorage.setItem('user', JSON.stringify({
        uuid: userStore.uuid,
        username: userStore.username,
        email: userStore.email,
        user_type: userStore.userType,
        name: name.value,
        avatar: userStore.avatar,
        token: userStore.token
      }))
      errors.value = null
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    profileUpdating.value = false
  }
}

watch(country, (newValue, oldValue) => {
  if (oldValue) {
    city.value = null
  }
})

onMounted(async () => {
  await getProfileData()
})
</script>

<template>
  <div
    v-if="profileLoading"
    class="d-flex justify-center align-center my-15"
  >
    <v-progress-circular
      indeterminate
      :size="80"
    ></v-progress-circular>
  </div>

  <v-form
    v-else
    @submit.prevent="updateProfile()"
    class="mt-9 mb-10"
  >
    <v-row dense>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-text-field
          v-model="name"
          :readonly="profileUpdating"
          type="text"
          maxlength="255"
          variant="filled"
          :label="$t('user.name')"
          :error-messages="errors?.user?.name ? errors.user.name : []"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="12"
        :md="6"
      >
        <v-autocomplete
          v-model="country"
          :items="countryOptions"
          item-title="title"
          item-value="value"
          :no-data-text="$t('form_help.no_options_available')"
          :readonly="profileUpdating"
          clearable
          variant="filled"
          :label="$t('user.country')"
          :error-messages="errors?.user?.country ? errors.user.country : []"
        ></v-autocomplete>
      </v-col>
      <v-col
        :cols="12"
        :md="6"
      >
        <v-autocomplete
          v-model="city"
          :items="cityOptions"
          item-title="title"
          item-value="value"
          :no-data-text="$t('form_help.no_options_available')"
          :readonly="profileUpdating"
          clearable
          variant="filled"
          :label="$t('user.city')"
          :error-messages="errors?.user?.city ? errors.user.city : []"
        ></v-autocomplete>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-text-field
          v-model="phone"
          :readonly="profileUpdating"
          type="tel"
          maxlength="21"
          variant="filled"
          :label="$t('user.phone')"
          :error-messages="errors?.user?.phone ? errors.user.phone : []"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-text-field
          v-model="dateOfWedding"
          :readonly="profileUpdating"
          variant="filled"
          type="date"
          :label="$t('user.date_of_wedding')"
          :error-messages="errors?.date_of_wedding ? errors.date_of_wedding : []"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-btn
          :loading="profileUpdating"
          type="submit"
          variant="flat"
          color="primary"
          size="x-large"
          class="text-none"
        >
          {{ $t('user.update_profile') }}
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
