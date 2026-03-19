<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import NotFound from '@/components/NotFound.vue'
import FavoriteListItem from '@/components/FavoriteListItem.vue'
import ReportListItemDialog from '@/components/ReportListItemDialog.vue'
import CommentList from '@/components/comments/CommentList.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const photoLoading = ref(true)
const photoData = ref({
  author: {
    name: '',
    avatar: null,
    profile_url: null
  },
  album: null,
  image: null,
  device: '',
  f_number: 0.00,
  exposure_time: '',
  focal_length: 0.00,
  photographic_sensitivity: 0,
  title: '',
  description: '',
  tags: [],
  uploaded_at: null,
  view_count: 0,
  like_count: 0,
  liked: null,
  rating: 0.0,
  favorite: null,
  prev_photo_uuid: null,
  next_photo_uuid: null
})

const { getLocaleDateString } = useLocaleDateTime()

const upViewCountTimeout = ref(null)
const errorStatus = ref(null)

useSeoMeta({
  title: () => {
    return photoData.value.title
      ? photoData.value.title
      : t('seo_meta.photo_list.title')
  },
  ogTitle: () => {
    return photoData.value.title
      ? photoData.value.title
      : t('seo_meta.photo_list.title')
  },
  description: () => {
    return photoData.value.description
      ? photoData.value.description
      : t('seo_meta.photo_list.description')
  },
  ogDescription: () => {
    return photoData.value.description
      ? photoData.value.description
      : t('seo_meta.photo_list.description')
  }
})

const upPhotoViewCount = async () => {
  try {
    const response = await axios.post(
      '/portfolio/photo/up-view-count/'
        + route.params.uuid
        + '/'
    )
    photoData.value.view_count += 1
  } catch (error) {
    console.error(error)
  }
}

const getPhotoData = async () => {
  photoLoading.value = true

  let params = new URLSearchParams()
  if (route.query.from === 'popular') {
    params.append('ordering', '-rating')
  } else if (route.query.from === 'fresh') {
    params.append('ordering', '-uploaded_at')
  } else if (route.query.from === 'editors') {
    params.append('editors_choice', true)
  } else if (route.query.from === 'album') {
    params.append('album', route.query.album)
  } else if (route.query.from === 'author') {
    params.append('author', route.query.author)
    params.append('album_is_null', true)
  } else if (route.query.from === 'tags') {
    params.append('tags', route.query.tags)
  } else {
    params.append('ordering', 'rating')
  }

  try {
    const response = await axios.get(
      '/portfolio/photo/retrieve/'
        + route.params.uuid
        + '/',
      { params: params }
    )
    photoData.value = response.data
    upViewCountTimeout.value = setTimeout(upPhotoViewCount, 3000)
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    photoLoading.value = false
  }
}

const likePhoto = async () => {
  try {
    const response = await axios.post(
      '/portfolio/photo/like/'
        + route.params.uuid
        + '/'
    )
    if (response.status === 204) {
      photoData.value.like_count += 1
      photoData.value.liked = true
    }
  } catch (error) {
    console.error(error)
  }
}

const dislikePhoto = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/photo/like/'
        + route.params.uuid
        + '/'
    )
    if (response.status === 204) {
      photoData.value.like_count -= 1
      photoData.value.liked = false
    }
  } catch (error) {
    console.error(error)
  }
}

const keyUpArrowLeftRight = (event) => {
  if (event.keyCode === 37 && photoData.value.prev_photo_uuid) {
    router.push({
      params: { uuid: photoData.value.prev_photo_uuid },
      query: route.query
    })
  } else if (event.keyCode === 39 && photoData.value.next_photo_uuid) {
    router.push({
      params: { uuid: photoData.value.next_photo_uuid },
      query: route.query
    })
  }
}

watch(
  () => route.params.uuid,
  async () => {
    if (route.name === 'PhotoDetail') {
      errorStatus.value = null
      await getPhotoData()
    }
  }
)

onMounted(async () => {
  await getPhotoData()
  window.addEventListener('keyup', keyUpArrowLeftRight)
})

onUnmounted(() => {
  clearTimeout(upViewCountTimeout.value)
  window.removeEventListener('keyup', keyUpArrowLeftRight)
})
</script>

<template>
  <v-container>
    <div
      v-if="photoLoading"
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
      <v-hover v-slot="{ isHovering, props }">
        <v-sheet
          v-bind="props"
          position="relative"
          style="z-index: 0;"
        >
          <v-img
            :src="photoData.image"
            :alt="photoData.title"
            max-width="100%"
            max-height="75vh"
          ></v-img>
          <v-overlay
            :model-value="isHovering"
            contained
            :opacity="0"
            content-class="d-flex justify-space-between align-center w-100 h-100 pa-3"
          >
            <v-btn
              :to="{
                params: { uuid: photoData.prev_photo_uuid },
                query: $route.query
              }"
              :disabled="!photoData.prev_photo_uuid"
              icon="mdi-chevron-left"
              :elevation="1"
            ></v-btn>
            <v-btn
              :to="{
                params: { uuid: photoData.next_photo_uuid },
                query: $route.query
              }"
              :disabled="!photoData.next_photo_uuid"
              icon="mdi-chevron-right"
              :elevation="1"
            ></v-btn>
          </v-overlay>
        </v-sheet>
      </v-hover>

      <v-row
        dense
        class="my-3"
      >
        <v-col
          :cols="12"
          :lg="7"
        >
          <div class="elevation-1 rounded-lg pa-5">
            <v-row dense>
              <v-col
                :cols="12"
                :md="8"
              >
                <div class="d-flex justify-center justify-md-start">
                  <div class="d-inline-block">
                    <h1
                      v-if="photoData.title"
                      class="text-h5"
                    >
                      {{ photoData.title }}
                    </h1>

                    <div class="d-flex flex-wrap ga-5 mt-3">
                      <div class="d-flex align-center text-secondary">
                        <v-icon
                          icon="mdi-calendar-month-outline"
                          :size="24"
                          class="me-1"
                        ></v-icon>
                        {{ $t('portfolio.uploaded') }}
                        {{ getLocaleDateString(photoData.uploaded_at) }}
                      </div>
                      <div class="d-flex align-center text-secondary">
                        <v-icon
                          icon="mdi-eye-outline"
                          :size="24"
                          class="me-1"
                        ></v-icon>
                        {{ photoData.view_count }}
                      </div>
                      <div class="d-flex align-center text-secondary">
                        <v-icon
                          icon="mdi-star-outline"
                          :size="24"
                          class="me-1"
                        ></v-icon>
                        {{ photoData.rating.toFixed(1) }}
                      </div>
                    </div>
                  </div>
                </div>
              </v-col>
              <v-col
                :cols="12"
                :md="4"
              >
                <div
                  v-if="userStore.isLoggedIn"
                  class="d-flex justify-center justify-md-end align-center"
                >
                  <v-tooltip
                    location="start"
                    :text="`${photoData.like_count}`"
                  >
                    <template v-slot:activator="{ props }">
                      <v-btn
                        v-bind="props"
                        :icon="photoData.liked ? 'mdi-heart' : 'mdi-heart-outline'"
                        @click="photoData.liked ? dislikePhoto() : likePhoto()"
                        variant="text"
                        color="primary"
                      ></v-btn>
                    </template>
                  </v-tooltip>

                  <v-menu
                    location="start"
                    :close-on-content-click="false"
                  >
                    <template v-slot:activator="{ props }">
                      <v-btn
                        v-bind="props"
                        icon="mdi-dots-horizontal"
                        variant="text"
                      ></v-btn>
                    </template>
                    <template v-slot:default="{ isActive }">
                      <v-list density="compact">
                        <FavoriteListItem
                          :objFavorite="photoData.favorite"
                          contentType="photo"
                          :objectUUID="$route.params.uuid"
                          @favoriteUpdated="(status) => {
                            photoData.favorite = status
                            isActive.value = false
                          }"
                        />
                        <ReportListItemDialog
                          contentType="photo"
                          :objectUUID="$route.params.uuid"
                          @reportSent="isActive.value = false"
                        />
                      </v-list>
                    </template>
                  </v-menu>
                </div>
              </v-col>
            </v-row>

            <v-row dense>
              <v-col
                :cols="12"
                :md="6"
              >
                <div class="d-flex justify-center justify-md-start align-center">
                  <router-link
                    :to="{
                      name: 'OrganizerDetail',
                      params: { profile_url: photoData.author.profile_url }
                    }"
                  >
                    <v-avatar :size="32">
                      <v-img
                        v-if="photoData.author.avatar"
                        :src="photoData.author.avatar"
                      ></v-img>
                      <v-icon
                        v-else
                        icon="mdi-account-circle"
                        :size="32"
                        role="img"
                      ></v-icon>
                    </v-avatar>
                  </router-link>
                  <router-link
                    :to="{
                      name: 'OrganizerDetail',
                      params: { profile_url: photoData.author.profile_url }
                    }"
                    class="text-body-1 text-decoration-none text-black ms-1"
                  >
                    {{ photoData.author.name }}
                  </router-link>
                </div>
              </v-col>
              <v-col
                :cols="12"
                :md="6"
              >
                <div
                  v-if="photoData.album"
                  class="d-flex justify-center justify-md-end align-center"
                >
                  <router-link
                    :to="{
                      name: 'AlbumDetail',
                      params: { uuid: photoData.album.uuid }
                    }"
                  >
                    <v-img
                      :src="photoData.album.thumbnail"
                      :width="32"
                      :aspect-ratio="1/1"
                      cover
                      class="rounded-circle"
                    ></v-img>
                  </router-link>
                  <router-link
                    :to="{
                      name: 'AlbumDetail',
                      params: { uuid: photoData.album.uuid }
                    }"
                    class="text-body-1 text-decoration-none text-black ms-1"
                  >
                    {{ photoData.album.title }}
                  </router-link>
                </div>
              </v-col>
            </v-row>

            <p
              v-if="photoData.description"
              class="text-body-1 mt-3"
            >
              {{ photoData.description }}
            </p>
          </div>

          <div
            v-if="photoData.device"
            class="elevation-1 rounded-lg pa-5 my-2"
          >
            <div class="d-flex align-center">
              <v-icon
                icon="mdi-camera"
                :size="24"
                class="me-1"
              ></v-icon>
              {{ photoData.device }}
            </div>
            <div
              v-if="
                photoData.f_number
                  || photoData.exposure_time
                  || photoData.focal_length
                  || photoData.photographic_sensitivity
              "
              class="d-flex flex-wrap ga-3"
            >
              <span v-if="photoData.f_number">
                f/{{ photoData.f_number }}
              </span>
              <span v-if="photoData.exposure_time">
                {{ photoData.exposure_time }}s
              </span>
              <span v-if="photoData.focal_length">
                {{ photoData.focal_length }}mm
              </span>
              <span v-if="photoData.photographic_sensitivity">
                ISO {{ photoData.photographic_sensitivity }}
              </span>
            </div>
          </div>

          <div
            v-if="photoData.tags.length > 0"
            class="elevation-1 rounded-lg pa-5 my-2"
          >
            <div class="d-flex flex-wrap ga-2">
              <v-btn
                v-for="tag in photoData.tags"
                :key="tag.uuid"
                :to="{
                  name: 'TagDetail',
                  params: { uuid: tag.uuid },
                  query: { tab: 'photos' }
                }"
                prepend-icon="mdi-pound"
                variant="tonal"
                class="text-none"
              >
                {{ tag.name }}
              </v-btn>
            </div>
          </div>
        </v-col>
        <v-col
          :cols="12"
          :lg="5"
        >
          <div
            class="elevation-1 rounded-lg overflow-y-auto pa-3"
            style="max-height: 75vh;"
          >
            <CommentList
              contentType="photo"
              :objectUUID="$route.params.uuid"
            />
          </div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 0.3em;
}
</style>
