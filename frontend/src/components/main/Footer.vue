<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { LANGUAGES, CURRENCIES } from '@/config.js'
import { useCurrencyStore } from '@/stores/currency.js'

const { t } = useI18n({ useScope: 'global' })
const route = useRoute()
const router = useRouter()
const currencyStore = useCurrencyStore()

const magazineDataLoading = ref(true)
const magazineData = ref({})

const currencyOptions = computed(() => {
  return Array.from(CURRENCIES, (element) => {
    return {
      value: element.value,
      title: t(`currencies.${element.value}`)
    }
  })
})

const getMagazine = async () => {
  try {
    const response = await axios.get('/main/magazine/')
    magazineData.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    magazineDataLoading.value = false
  }
}

const changeLocale = (value) => {
  router.push({
    params: { locale: value },
    query: route.query
  })
}

const changeCurrency = (value) => {
  window.localStorage.setItem('currency', value)
  currencyStore.setCurrency(value)
}

onMounted(async () => {
  await getMagazine()
})
</script>

<template>
  <v-footer class="bg-grey-darken-4 text-white">
    <v-container class="pt-10">
      <v-row class="pb-5">
        <v-col
          :cols="12"
          :sm="3"
        >
          <div
            v-if="magazineDataLoading"
            class="d-flex justify-center align-center h-100"
          >
            <v-progress-circular indeterminate></v-progress-circular>
          </div>
          <a
            v-else
            :href="magazineData.file"
            :title="magazineData.title"
            target="_blank"
          >
            <img
              :src="magazineData.image"
              height="160"
            >
          </a>
        </v-col>
        <v-col
          :cols="12"
          :sm="3"
        >
          <ul class="d-flex flex-column">
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.rules') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.advertising') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.our_logos') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'Feedback',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('feedback.feedback') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'About',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.more_about_magwed') }}
              </router-link>
            </li>
          </ul>
        </v-col>
        <v-col
          :cols="12"
          :sm="3"
        >
          <ul class="d-flex flex-column">
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.analytics') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.career_at_magwed') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.terms_of_use') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.privacy_policy') }}
              </router-link>
            </li>
            <li>
              <router-link
                :to="{
                  name: 'Home',
                  params: { locale: $i18n.locale }
                }"
                class="d-block text-decoration-none text-white py-1"
              >
                {{ $t('footer.advertising_and_promotion') }}
              </router-link>
            </li>
          </ul>
        </v-col>
        <v-col
          :cols="12"
          :sm="3"
        >
          <ul class="d-flex flex-column">
            <li>
              <v-select
                :model-value="$i18n.locale"
                @update:modelValue="changeLocale"
                :items="LANGUAGES"
                item-title="title"
                item-value="value"
                variant="outlined"
                density="comfortable"
              ></v-select>
            </li>
            <li>
              <v-select
                :model-value="currencyStore.currencyValue"
                @update:modelValue="changeCurrency"
                :items="currencyOptions"
                item-title="title"
                item-value="value"
                variant="outlined"
                density="comfortable"
              ></v-select>
            </li>
          </ul>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row class="d-flex flex-md-row-reverse pt-5">
        <v-col
          :cols="12"
          :sm="6"
          class="d-flex justify-center justify-md-end"
        >
          <a
            class="text-secondary link-facebook me-3"
            href="https://www.facebook.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-facebook"
              size="small"
            ></v-icon>
          </a>
          <a
            class="text-secondary link-twitter me-3"
            href="https://twitter.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-twitter"
              size="small"
            ></v-icon>
          </a>
          <a
            class="text-secondary link-instagram me-3"
            href="https://www.instagram.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-instagram"
              size="small"
            ></v-icon>
          </a>
          <a
            class="text-secondary link-linkedin me-3"
            href="https://www.linkedin.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-linkedin"
              size="small"
            ></v-icon>
          </a>
          <a
            class="text-secondary link-spotify me-3"
            href="https://www.spotify.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-spotify"
              size="small"
            ></v-icon>
          </a>
          <a
            class="text-secondary link-youtube me-3"
            href="https://www.youtube.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-youtube"
              size="small"
            ></v-icon>
          </a>
          <a
            class="text-secondary link-soundcloud me-3"
            href="https://soundcloud.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-soundcloud"
              size="small"
            ></v-icon>
          </a>
          <a
            class="text-secondary link-pinterest"
            href="https://www.pinterest.com/"
            target="_blank"
          >
            <v-icon
              icon="mdi-pinterest"
              size="small"
            ></v-icon>
          </a>
        </v-col>
        <v-col
          :cols="12"
          :sm="6"
          class="d-flex justify-center justify-md-start text-secondary"
        >
          Copyright © 2022—{{ new Date().getFullYear() }} MAGWED
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<style scoped>
ul {
  list-style: none;
}
ul > li a:focus,
ul > li a:hover {
  color: #e72a26 !important;
}
</style>
