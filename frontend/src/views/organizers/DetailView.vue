<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useRoute } from 'vue-router'
import { ref, computed, watch, onMounted } from 'vue'
import { useCurrencyStore } from '@/stores/currency.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import AlbumList from '@/components/organizers/AlbumList.vue'
import PhotoList from '@/components/organizers/PhotoList.vue'
import ReviewList from '@/components/organizers/ReviewList.vue'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()
const currencyStore = useCurrencyStore()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const organizerLoading = ref(true)
const organizerData = ref({
  user: {
    uuid: '',
    email: '',
    name: '',
    avatar: null,
    country: null,
    city: null,
    phone: '',
    date_joined: null,
    status: null,
    following: null
  },
  roles: [],
  cover: null,
  description: '',
  countries: [],
  cities: [],
  languages: [],
  cost_work: 0.0,
  number_hours: 0,
  website: '',
  rating: 0.0
})

const writeMessageDialog = ref(false)
const messageSending = ref(false)
const textContent = ref('')

const mediaToggle = ref('photos')

const { getLocaleDateString, getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)
const errorStatus = ref(null)

const organizerWebsiteShort = computed(() => {
  return organizerData.value.website.split('://')[1]
})

useSeoMeta({
  title: () => organizerData.value.user.name,
  ogTitle: () => organizerData.value.user.name,
  description: () => organizerData.value.description,
  ogDescription: () => organizerData.value.description
})

const getOrganizerData = async () => {
  organizerLoading.value = true
  try {
    const response = await axios.get(
      '/accounts/organizers/'
        + route.params.profile_url
        + '/'
    )
    organizerData.value = response.data
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    organizerLoading.value = false
  }
}

const updateUserStatus = (mutation, state) => {
  if (organizerData.value.user.uuid === state.user_uuid) {
    organizerData.value.user.status = state.status
  }
}

const followUser = async () => {
  try {
    const response = await axios.post(
      '/social/follow/user/'
        + organizerData.value.user.uuid
        + '/'
    )
    if (response.status === 201) {
      organizerData.value.user.following = true
    }
  } catch (error) {
    console.error(error)
  }
}

const unfollowUser = async () => {
  try {
    const response = await axios.delete(
      '/social/follow/user/'
        + organizerData.value.user.uuid
        + '/'
    )
    if (response.status === 204) {
      organizerData.value.user.following = false
    }
  } catch (error) {
    console.error(error)
  }
}

const writeMessage = async () => {
  messageSending.value = true
  try {
    const response = await axios.post(
      '/messenger/message/write/'
        + organizerData.value.user.uuid
        + '/',
      { content: textContent.value }
    )
    if (response.status === 201) {
      writeMessageDialog.value = false
      textContent.value = ''
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

watch(
  () => route.params.profile_url,
  async () => {
    if (route.name === 'OrganizerDetail') {
      errorStatus.value = null
      await getOrganizerData()
    }
  }
)

onMounted(async () => {
  await getOrganizerData()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <v-container>
    <div
      v-if="organizerLoading"
      class="d-flex justify-center align-center my-15"
    >
      <v-progress-circular
        indeterminate
        :size="80"
      ></v-progress-circular>
    </div>

    <NotFound v-else-if="errorStatus === 404" />

    <div
      v-else
      class="my-5"
    >
      <v-sheet
        :elevation="1"
        rounded="lg"
        class="pb-5"
      >
        <v-img
          :src="organizerData.cover ? organizerData.cover : '/cover.jpg'"
          :aspect-ratio="3/1"
          cover
          rounded="t-lg"
        ></v-img>
        <div class="d-md-flex justify-md-start text-center mx-3 mx-md-5 mx-lg-8">
          <v-avatar
            :image="
              organizerData.user.avatar
                ? organizerData.user.avatar
                : '/user-avatar.png'
            "
            :size="180"
            class="position-relative"
            style="
              margin-top: -80px;
              border: 3px solid white;
            "
          ></v-avatar>

          <div class="d-inline-block mt-3 ms-md-3">
            <h1 class="text-h3">{{ organizerData.user.name }}</h1>

            <span
              v-if="organizerData.user.status === 'online'"
              class="d-flex align-center text-black"
            >
              <v-icon
                icon="mdi-circle"
                :size="16"
                color="green-darken-3"
                class="me-1"
              ></v-icon>
              {{ $t('user.online') }}
            </span>

            <span
              v-else
              class="d-flex align-center text-secondary"
            >
              <v-icon
                icon="mdi-circle"
                :size="16"
                class="me-1"
              ></v-icon>
              {{ $t('user.last_visit') }}
              {{ getLocaleDateTimeString(organizerData.user.status) }}
            </span>
          </div>
          <div
            v-if="
              userStore.isLoggedIn
                && userStore.uuid != organizerData.user.uuid
            "
            class="d-md-flex ms-md-auto text-center mt-3"
          >
            <v-btn
              :prepend-icon="
                organizerData.user.following
                  ? 'mdi-account-minus'
                  : 'mdi-account-plus'
              "
              @click="
                organizerData.user.following
                  ? unfollowUser()
                  : followUser()
              "
              :text="
                organizerData.user.following
                  ? $t('follow.unfollow')
                  : $t('follow.follow')
              "
              :variant="organizerData.user.following ? 'flat' : 'outlined'"
              color="primary"
              class="me-1"
            ></v-btn>

            <v-dialog
              v-model="writeMessageDialog"
              :max-width="500"
            >
              <template v-slot:activator="{ props: activatorProps }">
                <v-btn
                  v-bind="activatorProps"
                  prepend-icon="mdi-pen"
                  variant="tonal"
                >
                  {{ $t('messenger.write') }}
                </v-btn>
              </template>

              <v-card
                :title="$t('messenger.new_message')"
                rounded="lg"
              >
                <v-textarea
                  v-model="textContent"
                  :readonly="messageSending"
                  autofocus
                  auto-grow
                  :rows="5"
                  :max-rows="10"
                  variant="filled"
                  :label="$t('messenger.content')"
                  :error-messages="errors?.content ? errors.content : []"
                  class="mt-3 mx-3"
                ></v-textarea>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn @click="writeMessageDialog = false">
                    {{ $t('btn.cancel') }}
                  </v-btn>
                  <v-btn
                    @click="writeMessage()"
                    :loading="messageSending"
                    :disabled="!textContent"
                    variant="flat"
                    color="primary"
                  >
                    {{ $t('btn.send') }}
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
        </div>

        <div class="d-flex flex-wrap ga-1 mt-3 mx-3 mx-md-5 mx-lg-8">
          <v-chip
            v-for="roleValue in organizerData.roles"
            :key="roleValue"
          >
            {{ $t(`roles.${roleValue}`) }}
          </v-chip>
        </div>

        <div class="d-flex flex-wrap ga-3 mt-3 mx-3 mx-md-5 mx-lg-8">
          <div class="d-flex align-center">
            <v-icon
              icon="mdi-calendar-plus-outline"
              :size="24"
              class="me-1"
            ></v-icon>
            {{ $t('user.joined_on') }}
            {{ getLocaleDateString(organizerData.user.date_joined) }}
          </div>
          <div
            v-if="organizerData.user.city"
            class="d-flex align-center"
          >
            <v-icon
              icon="mdi-map-marker-outline"
              :size="24"
              class="me-1"
            ></v-icon>
            {{ $t(`cities.${organizerData.user.city}`) }},
            {{ $t(`countries.${organizerData.user.country}`) }}
          </div>
          <div
            v-else-if="organizerData.user.country"
            class="d-flex align-center"
          >
            <v-icon
              icon="mdi-map-marker-outline"
              :size="24"
              class="me-1"
            ></v-icon>
            {{ $t(`countries.${organizerData.user.country}`) }}
          </div>
          <div
            v-if="organizerData.user.phone"
            class="d-flex align-center"
          >
            <v-icon
              icon="mdi-phone-outline"
              :size="24"
              class="me-1"
            ></v-icon>
            <a
              :href="`tel:${organizerData.user.phone}`"
              class="text-decoration-none text-black"
            >
              {{ organizerData.user.phone }}
            </a>
          </div>
          <div
            v-if="organizerData.website"
            class="d-flex align-center"
          >
            <v-icon
              icon="mdi-web"
              :size="24"
              class="me-1"
            ></v-icon>
            <a
              :href="organizerData.website"
              class="text-decoration-none text-black"
            >
              {{ organizerWebsiteShort }}
            </a>
          </div>
        </div>
      </v-sheet>

      <v-sheet
        :elevation="1"
        rounded="lg"
        class="my-5 pa-3 pa-md-5"
      >
        <p
          v-if="organizerData.description"
          class="text-body-1"
        >
          {{ organizerData.description }}
        </p>

        <v-list>
          <v-list-item
            v-if="organizerData.countries.length"
            prepend-icon="mdi-earth"
          >
            {{ $t('user.countries') }}:
            <v-chip
              v-for="countryValue in organizerData.countries"
              :key="countryValue"
              size="small"
              class="ma-1"
            >
              {{ $t(`countries.${countryValue}`) }}
            </v-chip>
          </v-list-item>
          <v-list-item
            v-if="organizerData.cities.length"
            prepend-icon="mdi-city-variant-outline"
          >
            {{ $t('user.cities') }}:
            <v-chip
              v-for="cityValue in organizerData.cities"
              :key="cityValue"
              size="small"
              class="ma-1"
            >
              {{ $t(`cities.${cityValue}`) }}
            </v-chip>
          </v-list-item>
          <v-list-item
            v-if="organizerData.languages.length"
            prepend-icon="mdi-translate"
          >
            {{ $t('user.languages') }}:
            <v-chip
              v-for="languageValue in organizerData.languages"
              :key="languageValue"
              size="small"
              class="ma-1"
            >
              {{ $t(`languages.${languageValue}`) }}
            </v-chip>
          </v-list-item>
          <v-list-item
            v-if="organizerData.cost_work"
            prepend-icon="mdi-cash-multiple"
          >
            {{ $t('user.cost_work') }}:
            {{ currencyStore.currencySymbol }}{{ currencyStore.convertCurrency(organizerData.cost_work) }}
          </v-list-item>
          <v-list-item
            v-if="organizerData.number_hours"
            prepend-icon="mdi-clock-outline"
          >
            {{ $t('user.number_hours') }}:
            {{ organizerData.number_hours }}
          </v-list-item>
        </v-list>
      </v-sheet>

      <div class="text-center my-5">
        <v-btn-toggle
          v-model="mediaToggle"
          mandatory
          :rounded="0"
        >
          <v-btn value="photos">
            {{ $t('portfolio.photos') }}
          </v-btn>
          <v-btn value="albums">
            {{ $t('portfolio.photo_albums') }}
          </v-btn>
          <v-btn value="reviews">
            {{ $t('reviews.reviews') }}
          </v-btn>
        </v-btn-toggle>
      </div>

      <PhotoList
        v-if="mediaToggle === 'photos'"
        :userUUID="organizerData.user.uuid"
      />
      <AlbumList
        v-else-if="mediaToggle === 'albums'"
        :userUUID="organizerData.user.uuid"
      />
      <ReviewList
        v-else-if="mediaToggle === 'reviews'"
        :userUUID="organizerData.user.uuid"
      />
    </div>
  </v-container>
</template>
