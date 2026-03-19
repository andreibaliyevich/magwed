<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useOptionsOfRoleTypes } from '@/composables/optionsOfRoleTypes.js'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCities } from '@/composables/optionsOfCities.js'
import { useOptionsOfCitiesExtra } from '@/composables/optionsOfCitiesExtra.js'
import { useOptionsOfLanguages } from '@/composables/optionsOfLanguages.js'

const userStore = useUserStore()

const profileLoading = ref(true)
const profileUpdating = ref(false)

const name = ref('')
const country = ref(null)
const city = ref(null)
const phone = ref('')
const roles = ref([])
const description = ref('')
const countries = ref([])
const cities = ref([])
const languages = ref([])
const costWork = ref(0.00)
const numberHours = ref(0)
const website = ref('')
const profileURL = ref('')
const rating = ref(0.0)
const proTime = ref(null)

const { roleTypeOptions } = useOptionsOfRoleTypes('roles')
const { countryOptions } = useOptionsOfCountries()
const { cityOptions } = useOptionsOfCities(country)
const { cityOptionsExtra } = useOptionsOfCitiesExtra(countries)
const { languageOptions } = useOptionsOfLanguages()

const errors = ref(null)

const getProfileData = async () => {
  try {
    const response = await axios.get('/accounts/auth/profile/')
    name.value = response.data.user.name
    country.value = response.data.user.country
    city.value = response.data.user.city
    phone.value = response.data.user.phone
    roles.value = response.data.roles
    description.value = response.data.description
    countries.value = response.data.countries
    cities.value = response.data.cities
    languages.value = response.data.languages
    costWork.value = response.data.cost_work
    numberHours.value = response.data.number_hours
    website.value = response.data.website
    profileURL.value = response.data.profile_url
    rating.value = response.data.rating
    proTime.value = response.data.pro_time
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

  try {
    const response = await axios.put('/accounts/auth/profile/', {
      user: {
        name: name.value,
        country: country.value,
        city: city.value,
        phone: phone.value
      },
      roles: roles.value,
      description: description.value,
      countries: countries.value,
      cities: cities.value,
      languages: languages.value,
      cost_work: costWork.value,
      number_hours: numberHours.value,
      website: website.value,
      profile_url: profileURL.value
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

watch(cityOptionsExtra, (newValue, oldValue) => {
  if (newValue.length < oldValue.length) {
    const newCitiesValues = newValue.map(element => element.value)
    cities.value = cities.value.filter((element) => {
      return newCitiesValues.includes(element)
    })
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
        <v-select
          v-model="roles"
          :items="roleTypeOptions"
          item-title="title"
          item-value="value"
          :readonly="profileUpdating"
          multiple
          clearable
          variant="filled"
          :label="$t('user.roles')"
          :error-messages="errors?.roles ? errors.roles : []"
        ></v-select>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-textarea
          v-model="description"
          :readonly="profileUpdating"
          :label="$t('user.description')"
          :error-messages="errors?.description ? errors.description : []"
        ></v-textarea>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-autocomplete
          v-model="countries"
          :items="countryOptions"
          item-title="title"
          item-value="value"
          :no-data-text="$t('form_help.no_options_available')"
          :readonly="profileUpdating"
          multiple
          clearable
          variant="filled"
          :label="$t('user.countries')"
          :error-messages="errors?.countries ? errors.countries : []"
        ></v-autocomplete>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-autocomplete
          v-model="cities"
          :items="cityOptionsExtra"
          item-title="title"
          item-value="value"
          :no-data-text="$t('form_help.no_options_available')"
          :readonly="profileUpdating"
          multiple
          clearable
          variant="filled"
          :label="$t('user.cities')"
          :error-messages="errors?.cities ? errors.cities : []"
        ></v-autocomplete>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-autocomplete
          v-model="languages"
          :items="languageOptions"
          item-title="title"
          item-value="value"
          :no-data-text="$t('form_help.no_options_available')"
          :readonly="profileUpdating"
          multiple
          clearable
          variant="filled"
          :label="$t('user.languages')"
          :error-messages="errors?.languages ? errors.languages : []"
        ></v-autocomplete>
      </v-col>
      <v-col
        :cols="12"
        :md="6"
      >
        <v-text-field
          v-model="costWork"
          :readonly="profileUpdating"
          type="number"
          min="0.00"
          step="0.01"
          variant="filled"
          :label="$t('user.cost_work')"
          prefix="$"
          :hint="$t('form_help.cost_work')"
          :error-messages="errors?.cost_work ? errors.cost_work : []"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="12"
        :md="6"
      >
        <v-text-field
          v-model="numberHours"
          :readonly="profileUpdating"
          type="number"
          min="0"
          variant="filled"
          :label="$t('user.number_hours')"
          :error-messages="errors?.number_hours ? errors.number_hours : []"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-text-field
          v-model="website"
          :readonly="profileUpdating"
          type="url"
          maxlength="200"
          variant="filled"
          :label="$t('user.website')"
          :error-messages="errors?.website ? errors.website : []"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="12"
        :md="12"
      >
        <v-text-field
          v-model="profileURL"
          :readonly="profileUpdating"
          type="text"
          maxlength="64"
          variant="filled"
          :label="$t('user.profile_url')"
          :error-messages="errors?.profile_url ? errors.profile_url : []"
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
