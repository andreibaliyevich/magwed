<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, computed, watch, onMounted } from 'vue'
import { useCurrencyStore } from '@/stores/currency.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import { useOptionsOfRoleTypes } from '@/composables/optionsOfRoleTypes.js'
import { useOptionsOfCountries } from '@/composables/optionsOfCountries.js'
import { useOptionsOfCitiesExtra } from '@/composables/optionsOfCitiesExtra.js'
import { useOptionsOfLanguages } from '@/composables/optionsOfLanguages.js'

const route = useRoute()
const { t } = useI18n({ useScope: 'global' })
const currencyStore = useCurrencyStore()
const connectionBusStore = useConnectionBusStore()

const organizerListLoading = ref(true)
const organizerList = ref([])
const nextURL = ref(null)

const countries = ref([])
const cities = ref([])
const languages = ref([])
const costWorkMin = ref(0)
const costWorkMax = ref(0)
const costWorkInCurrency = ref([0, 0])

const { roleTypeOptions } = useOptionsOfRoleTypes('plural_roles')
const { countryOptions } = useOptionsOfCountries()
const { cityOptionsExtra } = useOptionsOfCitiesExtra(countries)
const { languageOptions } = useOptionsOfLanguages()

const filterMenuDrawer = ref(false)

const costWorkMinBorder = computed(() => {
  return Math.floor(costWorkMin.value * currencyStore.conversionRate)
})
const costWorkMaxBorder = computed(() => {
  return Math.ceil(costWorkMax.value * currencyStore.conversionRate)
})

useSeoMeta({
  title: () => t('seo_meta.organizer_list.title'),
  ogTitle: () => t('seo_meta.organizer_list.title'),
  description: () => t('seo_meta.organizer_list.description'),
  ogDescription: () => t('seo_meta.organizer_list.description'),
  keywords: () => t('seo_meta.organizer_list.keywords'),
  ogKeywords: () => t('seo_meta.organizer_list.keywords')
})

const getOrganizerList = async () => {
  organizerListLoading.value = true
  organizerList.value = []
  filterMenuDrawer.value = false

  let params = new URLSearchParams()
  if (route.query.role) {
    params.append('roles', route.query.role)
  }
  countries.value.forEach((element) => params.append('countries', element))
  cities.value.forEach((element) => params.append('cities', element))
  languages.value.forEach((element) => params.append('languages', element))
  if (costWorkInCurrency.value[0]) {
    params.append('cost_work_min', Math.floor(
      costWorkInCurrency.value[0] / currencyStore.conversionRate
    ))
  }
  if (costWorkInCurrency.value[1]) {
    params.append('cost_work_max', Math.ceil(
      costWorkInCurrency.value[1] / currencyStore.conversionRate
    ))
  }

  try {
    const response = await axios.get('/accounts/organizers/', {
      params: params
    })
    organizerList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    organizerListLoading.value = false
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const getMoreOrganizerList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      organizerList.value = [...organizerList.value, ...response.data.results]
      nextURL.value = response.data.next
      done('ok')
    } catch (error) {
      console.error(error)
      done('error')
    }
  } else {
    done('empty')
  }
}

const getCostWorkMinMax = async () => {
  try {
    const response = await axios.get('/accounts/organizers/cost-work-min-max/')
    costWorkMin.value = response.data.cost_work_min
    costWorkMax.value = response.data.cost_work_max
    costWorkInCurrency.value[0] = Math.floor(
      response.data.cost_work_min * currencyStore.conversionRate
    )
    costWorkInCurrency.value[1] = Math.ceil(
      response.data.cost_work_max * currencyStore.conversionRate
    )
  } catch (error) {
    console.error(error)
  }
}

const resetParamsAndGetOrganizers = async () => {
  countries.value = []
  cities.value = []
  languages.value = []
  costWorkInCurrency.value[0] = Math.floor(
    costWorkMin.value * currencyStore.conversionRate
  )
  costWorkInCurrency.value[1] = Math.ceil(
    costWorkMax.value * currencyStore.conversionRate
  )
  getOrganizerList()
}

const updateUserStatus = (mutation, state) => {
  organizerList.value.forEach((element) => {
    if (element.user.uuid === state.user_uuid) {
      element.user.status = state.status
    }
  })
}

watch(
  () => route.query.role,
  async () => {
    if (route.name === 'OrganizerList') {
      await getOrganizerList()
    }
  }
)

watch(cityOptionsExtra, (newValue, oldValue) => {
  if (newValue.length < oldValue.length) {
    const newCitiesValues = newValue.map(element => element.value)
    cities.value = cities.value.filter((element) => {
      return newCitiesValues.includes(element)
    })
  }
})

watch(
  () => currencyStore.conversionRate,
  (newValue, oldValue) => {
    const newCostWorkMinInCurrency = Math.floor(
      costWorkInCurrency.value[0] * newValue / oldValue
    )
    costWorkInCurrency.value[0] =
      newCostWorkMinInCurrency < costWorkMinBorder.value
        ? costWorkMinBorder.value
        : newCostWorkMinInCurrency
    const newCostWorkMaxInCurrency = Math.ceil(
      costWorkInCurrency.value[1] * newValue / oldValue
    )
    costWorkInCurrency.value[1] =
      newCostWorkMaxInCurrency > costWorkMaxBorder.value
        ? costWorkMaxBorder.value
        : newCostWorkMaxInCurrency
  }
)

onMounted(async () => {
  await getOrganizerList()
  await getCostWorkMinMax()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('organizers.organizers') }}
    </h1>

    <v-slide-group
      :model-value="$route.query.role"
      show-arrows
    >
      <v-slide-group-item>
        <v-btn
          :to="{ name: 'OrganizerList' }"
          :active="!$route.query.role"
          variant="text"
          :value="undefined"
        >
          {{ $t('organizers.all') }}
        </v-btn>
      </v-slide-group-item>
      <v-slide-group-item
        v-for="roleType in roleTypeOptions"
        :key="roleType.value"
        :value="roleType.value"
      >
        <v-btn
          :to="{ query: { role: roleType.value } }"
          :active="$route.query.role == roleType.value"
          variant="text"
        >
          {{ roleType.title }}
        </v-btn>
      </v-slide-group-item>
    </v-slide-group>

    <v-row class="mt-3">
      <v-col
        :cols="12"
        :md="3"
      >
        <v-btn
          @click.stop="filterMenuDrawer = !filterMenuDrawer"
          variant="outlined"
          block
          class="d-inline-flex d-md-none"
          append-icon="mdi-filter-outline"
        >
          {{ $t('organizers.filters') }}
        </v-btn>
        <v-navigation-drawer
          v-model="filterMenuDrawer"
          location="end"
          temporary
        >
          <div class="pa-3">
            <h5 class="text-h6">{{ $t('organizers.filters') }}</h5>

            <p class="text-subtitle-1 mt-5 mb-2">{{ $t('user.countries') }}</p>
            <v-sheet
              :max-height="230"
              class="overflow-y-auto"
            >
              <v-checkbox
                v-for="country in countryOptions"
                :key="country.value"
                v-model="countries"
                :value="country.value"
                :label="country.title"
                :readonly="organizerListLoading"
                multiple
                density="compact"
                hide-details
              ></v-checkbox>
            </v-sheet>

            <p
              v-if="countries.length > 0"
              class="text-subtitle-1 mt-5 mb-2"
            >
              {{ $t('user.cities') }}
            </p>
            <v-sheet
              v-if="countries.length > 0"
              :max-height="230"
              class="overflow-y-auto"
            >
              <v-checkbox
                v-for="city in cityOptionsExtra"
                :key="city.value"
                v-model="cities"
                :value="city.value"
                :label="city.title"
                :readonly="organizerListLoading"
                multiple
                density="compact"
                hide-details
              ></v-checkbox>
            </v-sheet>

            <p class="text-subtitle-1 mt-5 mb-2">{{ $t('user.languages') }}</p>
            <v-sheet
              :max-height="230"
              class="overflow-y-auto"
            >
              <v-checkbox
                v-for="language in languageOptions"
                :key="language.value"
                v-model="languages"
                :value="language.value"
                :label="language.title"
                :readonly="organizerListLoading"
                multiple
                density="compact"
                hide-details
              ></v-checkbox>
            </v-sheet>

            <p class="text-subtitle-1 mt-5 mb-2">{{ $t('user.cost_work') }}</p>
            <v-row dense>
              <v-col
                :cols="12"
                :md="6"
              >
                <v-text-field
                  v-model="costWorkInCurrency[0]"
                  type="number"
                  :min="costWorkMinBorder"
                  :max="costWorkInCurrency[1]"
                  :readonly="organizerListLoading"
                  variant="solo-filled"
                  density="compact"
                  flat
                ></v-text-field>
              </v-col>
              <v-col
                :cols="12"
                :md="6"
              >
                <v-text-field
                  v-model="costWorkInCurrency[1]"
                  type="number"
                  :min="costWorkInCurrency[0]"
                  :max="costWorkMaxBorder"
                  :readonly="organizerListLoading"
                  variant="solo-filled"
                  density="compact"
                  flat
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row dense>
              <v-col
                :cols="12"
                :lg="6"
              >
                <v-btn
                  @click="resetParamsAndGetOrganizers()"
                  variant="flat"
                  block
                  class="text-none"
                  :disabled="
                    !countries.length
                      && !cities.length
                      && !languages.length
                      && (costWorkInCurrency[0] === costWorkMinBorder)
                      && (costWorkInCurrency[1] === costWorkMaxBorder)
                  "
                >
                  {{ $t('btn.reset') }}
                </v-btn>
              </v-col>
              <v-col
                :cols="12"
                :lg="6"
              >
                <v-btn
                  @click="getOrganizerList()"
                  variant="flat"
                  color="primary"
                  block
                  class="text-none"
                  :disabled="
                    !countries.length
                      && !cities.length
                      && !languages.length
                      && (costWorkInCurrency[0] === costWorkMinBorder)
                      && (costWorkInCurrency[1] === costWorkMaxBorder)
                  "
                >
                  {{ $t('btn.show') }}
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </v-navigation-drawer>

        <v-sheet
          :elevation="1"
          rounded="lg"
          class="d-none d-md-block position-sticky pa-3"
        >
          <h5 class="text-h6">{{ $t('organizers.filters') }}</h5>

          <p class="text-subtitle-1 mt-5 mb-2">{{ $t('user.countries') }}</p>
          <v-sheet
            :max-height="230"
            class="overflow-y-auto"
          >
            <v-checkbox
              v-for="country in countryOptions"
              :key="country.value"
              v-model="countries"
              :value="country.value"
              :label="country.title"
              :readonly="organizerListLoading"
              multiple
              density="compact"
              hide-details
            ></v-checkbox>
          </v-sheet>

          <p
            v-if="countries.length > 0"
            class="text-subtitle-1 mt-5 mb-2"
          >
            {{ $t('user.cities') }}
          </p>
          <v-sheet
            v-if="countries.length > 0"
            :max-height="230"
            class="overflow-y-auto"
          >
            <v-checkbox
              v-for="city in cityOptionsExtra"
              :key="city.value"
              v-model="cities"
              :value="city.value"
              :label="city.title"
              :readonly="organizerListLoading"
              multiple
              density="compact"
              hide-details
            ></v-checkbox>
          </v-sheet>

          <p class="text-subtitle-1 mt-5 mb-2">{{ $t('user.languages') }}</p>
          <v-sheet
            :max-height="230"
            class="overflow-y-auto"
          >
            <v-checkbox
              v-for="language in languageOptions"
              :key="language.value"
              v-model="languages"
              :value="language.value"
              :label="language.title"
              :readonly="organizerListLoading"
              multiple
              density="compact"
              hide-details
            ></v-checkbox>
          </v-sheet>

          <p class="text-subtitle-1 mt-5 mb-2">{{ $t('user.cost_work') }}</p>
          <v-row dense>
            <v-col
              :cols="12"
              :md="6"
            >
              <v-text-field
                v-model="costWorkInCurrency[0]"
                type="number"
                :min="costWorkMinBorder"
                :max="costWorkInCurrency[1]"
                :readonly="organizerListLoading"
                variant="solo-filled"
                density="compact"
                flat
              ></v-text-field>
            </v-col>
            <v-col
              :cols="12"
              :md="6"
            >
              <v-text-field
                v-model="costWorkInCurrency[1]"
                type="number"
                :min="costWorkInCurrency[0]"
                :max="costWorkMaxBorder"
                :readonly="organizerListLoading"
                variant="solo-filled"
                density="compact"
                flat
              ></v-text-field>
            </v-col>
          </v-row>
          <v-range-slider
            v-model="costWorkInCurrency"
            :min="costWorkMinBorder"
            :max="costWorkMaxBorder"
            :step="1"
          ></v-range-slider>

          <v-row dense>
            <v-col
              :cols="12"
              :lg="6"
            >
              <v-btn
                @click="resetParamsAndGetOrganizers()"
                variant="flat"
                block
                class="text-none"
                :disabled="
                  !countries.length
                    && !cities.length
                    && !languages.length
                    && (costWorkInCurrency[0] === costWorkMinBorder)
                    && (costWorkInCurrency[1] === costWorkMaxBorder)
                "
              >
                {{ $t('btn.reset') }}
              </v-btn>
            </v-col>
            <v-col
              :cols="12"
              :lg="6"
            >
              <v-btn
                @click="getOrganizerList()"
                variant="flat"
                color="primary"
                block
                class="text-none"
                :disabled="
                  !countries.length
                    && !cities.length
                    && !languages.length
                    && (costWorkInCurrency[0] === costWorkMinBorder)
                    && (costWorkInCurrency[1] === costWorkMaxBorder)
                "
              >
                {{ $t('btn.show') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-sheet>
      </v-col>
      <v-col
        :cols="12"
        :md="9"
      >
        <div
          v-if="organizerListLoading"
          class="d-flex justify-center align-center my-15"
        >
          <v-progress-circular
            indeterminate
            :size="80"
          ></v-progress-circular>
        </div>

        <v-infinite-scroll
          v-else-if="organizerList.length > 0"
          @load="getMoreOrganizerList"
          mode="intersect"
          :empty-text="$t('organizers.no_more_organizers')"
        >
          <v-row class="ma-0">
            <v-col
              v-for="organizer in organizerList"
              :key="organizer.user.uuid"
              :cols="12"
              :xs="12"
              :sm="6"
              :lg="4"
              :xl="2"
              class="text-center"
            >
              <router-link
                :to="{
                  name: 'OrganizerDetail',
                  params: { profile_url: organizer.user.profile_url }
                }"
                class="d-inline-block"
              >
                <AvatarExtended
                  :image="organizer.user.avatar"
                  :size="180"
                  :online="organizer.user.status === 'online' ? true : false"
                />
              </router-link>
              <router-link
                :to="{
                  name: 'OrganizerDetail',
                  params: { profile_url: organizer.user.profile_url }
                }"
                class="text-black text-decoration-none"
              >
                <h2 class="text-h5">{{ organizer.user.name }}</h2>
              </router-link>
              <p v-if="organizer.cost_work">
                {{ currencyStore.currencySymbol }}{{ currencyStore.convertCurrency(organizer.cost_work) }}
                {{ $t('organizers.per_hour') }}
                <small
                  v-if="organizer.number_hours"
                  class="text-secondary"
                >
                  {{ $t('organizers.min_number_hours', { n: organizer.number_hours }) }}
                </small>
              </p>
            </v-col>
          </v-row>
        </v-infinite-scroll>

        <v-alert
          v-else
          type="info"
          variant="tonal"
          class="my-5"
        >
          {{ $t('organizers.no_organizers_available') }}
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 0.2em;
}
.d-none.d-md-block.position-sticky {
  top: 82px;
}
</style>
