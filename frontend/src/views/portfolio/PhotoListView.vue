<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const route = useRoute()
const { t } = useI18n({ useScope: 'global' })

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

useSeoMeta({
  title: () => t('seo_meta.photo_list.title'),
  ogTitle: () => t('seo_meta.photo_list.title'),
  description: () => t('seo_meta.photo_list.description'),
  ogDescription: () => t('seo_meta.photo_list.description'),
  keywords: () => t('seo_meta.photo_list.keywords'),
  ogKeywords: () => t('seo_meta.photo_list.keywords')
})

const getPhotoList = async () => {
  photoListLoading.value = true
  photoList.value = []

  let params = new URLSearchParams()
  if (route.query.tab === 'popular') {
    params.append('ordering', '-rating')
  } else if (route.query.tab === 'fresh') {
    params.append('ordering', '-uploaded_at')
  } else if (route.query.tab === 'editors') {
    params.append('editors_choice', true)
  } else {
    params.append('ordering', 'rating')
  }

  try {
    const response = await axios.get('/portfolio/photo/list/', {
      params: params
    })
    photoList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    photoListLoading.value = false
  }
}

const getMorePhotoList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      photoList.value = [...photoList.value, ...response.data.results]
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

watch(
  () => route.query.tab,
  async () => {
    if (route.name === 'PhotoList') {
      await getPhotoList()
    }
  }
)

onMounted(async () => {
  await getPhotoList()
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('portfolio.photos') }}
    </h1>

    <div class="text-center mb-5">
      <v-btn
        :to="{ query: { tab: 'popular' } }"
        :active="
          $route.query.tab === 'popular'
            || $route.query.tab === undefined
        "
        variant="text"
      >
        {{ $t('portfolio.popular_photos') }}
      </v-btn>
      <v-btn
        :to="{ query: { tab: 'fresh' } }"
        :active="$route.query.tab === 'fresh'"
        variant="text"
      >
        {{ $t('portfolio.fresh_photos') }}
      </v-btn>
      <v-btn
        :to="{ query: { tab: 'editors' } }"
        :active="$route.query.tab === 'editors'"
        variant="text"
      >
        {{ $t('portfolio.editors_choice') }}
      </v-btn>
    </div>

    <div
      v-if="photoListLoading"
      class="d-flex justify-center align-center my-15"
    >
      <v-progress-circular
        indeterminate
        :size="80"
      ></v-progress-circular>
    </div>

    <v-infinite-scroll
      v-else-if="photoList.length > 0"
      @load="getMorePhotoList"
      mode="intersect"
      :empty-text="$t('portfolio.no_more_photos')"
    >
      <v-row
        dense
        class="ma-0"
      >
        <v-col
          v-for="photoItem in photoList"
          :key="photoItem.uuid"
          :cols="12"
          :sm="6"
          :md="4"
          :lg="3"
          :xl="2"
        >
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              v-bind="props"
              rounded="lg"
            >
              <v-img
                :src="photoItem.thumbnail"
                :alt="photoItem.title"
                :aspect-ratio="1/1"
                cover
              ></v-img>

              <v-overlay
                :model-value="isHovering"
                contained
                scrim="black"
                :opacity="0.5"
                content-class="w-100 h-100"
              >
                <router-link
                  :to="{
                    name: 'PhotoDetail',
                    params: { uuid: photoItem.uuid },
                    query: { from: $route.query.tab }
                  }"
                  class="d-flex flex-column text-decoration-none text-white w-100 h-100 pa-3"
                >
                  <router-link
                    :to="{
                      name: 'OrganizerDetail',
                      params: { profile_url: photoItem.author.profile_url }
                    }"
                    class="d-flex align-center text-decoration-none text-white"
                  >
                    <v-avatar :size="32">
                      <v-img
                        v-if="photoItem.author.avatar"
                        :src="photoItem.author.avatar"
                      ></v-img>
                      <v-icon
                        v-else
                        icon="mdi-account-circle"
                        :size="32"
                        role="img"
                      ></v-icon>
                    </v-avatar>
                    <div class="text-body-1 ms-1">
                      {{ photoItem.author.name }}
                    </div>
                  </router-link>

                  <h5 class="text-h6 text-center my-auto">
                    {{ photoItem.title }}
                  </h5>

                  <div class="d-flex justify-space-between">
                    <small>
                      <v-icon icon="mdi-eye-outline"></v-icon>
                      {{ photoItem.view_count }}
                    </small>
                    <small>
                      <v-icon icon="mdi-heart-outline"></v-icon>
                      {{ photoItem.like_count }}
                    </small>
                    <small>
                      <v-icon icon="mdi-star-outline"></v-icon>
                      {{ photoItem.rating.toFixed(1) }}
                    </small>
                  </div>
                </router-link>
              </v-overlay>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </v-infinite-scroll>

    <v-alert
      v-else
      type="info"
      variant="tonal"
      class="my-5"
    >
      {{ $t('portfolio.no_photos') }}
    </v-alert>
  </v-container>
</template>
