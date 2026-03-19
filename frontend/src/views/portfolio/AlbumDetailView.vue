<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import NotFound from '@/components/NotFound.vue'
import FavoriteListItem from '@/components/FavoriteListItem.vue'
import ReportListItemDialog from '@/components/ReportListItemDialog.vue'
import CommentList from '@/components/comments/CommentList.vue'

const route = useRoute()
const { t } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const albumDataLoading = ref(true)
const albumData = ref({
  author: {
    name: '',
    avatar: null,
    profile_url: null
  },
  image: null,
  title: '',
  description: '',
  tags: [],
  created_at: null,
  view_count: 0,
  like_count: 0,
  liked: null,
  rating: 0.0,
  favorite: null
})

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const upViewCountTimeout = ref(null)
const errorStatus = ref(null)

useSeoMeta({
  title: () => {
    return albumData.value.title
      ? albumData.value.title
      : t('seo_meta.album_list.title')
  },
  ogTitle: () => {
    return albumData.value.title
      ? albumData.value.title
      : t('seo_meta.album_list.title')
  },
  description: () => {
    return albumData.value.description
      ? albumData.value.description
      : t('seo_meta.album_list.description')
  },
  ogDescription: () => {
    return albumData.value.description
      ? albumData.value.description
      : t('seo_meta.album_list.description')
  }
})

const getPhotoList = async () => {
  try {
    const response = await axios.get('/portfolio/photo/list/', {
      params: {
        album: route.params.uuid
      }
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

const upAlbumViewCount = async () => {
  try {
    const response = await axios.post(
      '/portfolio/album/up-view-count/'
        + route.params.uuid
        + '/'
    )
    albumData.value.view_count += 1
  } catch (error) {
    console.error(error)
  }
}

const getAlbumData = async () => {
  albumDataLoading.value = true
  try {
    const response = await axios.get(
      '/portfolio/album/retrieve/'
        + route.params.uuid
        + '/'
    )
    albumData.value = response.data
    getPhotoList()
    upViewCountTimeout.value = setTimeout(upAlbumViewCount, 3000)
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    albumDataLoading.value = false
  }
}

const likeAlbum = async () => {
  try {
    const response = await axios.post(
      '/portfolio/album/like/'
        + route.params.uuid
        + '/'
    )
    if (response.status === 204) {
      albumData.value.like_count += 1
      albumData.value.liked = true
    }
  } catch (error) {
    console.error(error)
  }
}

const dislikeAlbum = async () => {
  try {
    const response = await axios.delete(
      '/portfolio/album/like/'
        + route.params.uuid
        + '/'
    )
    if (response.status === 204) {
      albumData.value.like_count -= 1
      albumData.value.liked = false
    }
  } catch (error) {
    console.error(error)
  }
}

watch(
  () => route.params.uuid,
  async () => {
    if (route.name === 'AlbumDetail') {
      errorStatus.value = null
      await getAlbumData()
    }
  }
)

onMounted(async () => {
  await getAlbumData()
})

onUnmounted(() => {
  clearTimeout(upViewCountTimeout.value)
})
</script>

<template>
  <v-container>
    <div
      v-if="albumDataLoading"
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
          :src="albumData.image"
          rounded="t-lg"
        ></v-img>

        <v-row
          dense
          class="mx-5 my-3"
        >
          <v-col
            :cols="12"
            :md="8"
          >
            <div class="d-flex justify-center justify-md-start">
              <div class="d-inline-block">
                <h1 class="text-h5">{{ albumData.title }}</h1>

                <div class="d-flex flex-wrap ga-5 mt-3">
                  <div class="d-flex align-center text-secondary">
                    <v-icon
                      icon="mdi-calendar-month-outline"
                      :size="24"
                      class="me-1"
                    ></v-icon>
                    {{ $t('portfolio.created') }}
                    {{ getLocaleDateString(albumData.created_at) }}
                  </div>
                  <div class="d-flex align-center text-secondary">
                    <v-icon
                      icon="mdi-eye-outline"
                      :size="24"
                      class="me-1"
                    ></v-icon>
                    {{ albumData.view_count }}
                  </div>
                  <div class="d-flex align-center text-secondary">
                    <v-icon
                      icon="mdi-star-outline"
                      :size="24"
                      class="me-1"
                    ></v-icon>
                    {{ albumData.rating.toFixed(1) }}
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
                :text="`${albumData.like_count}`"
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    :icon="albumData.liked ? 'mdi-heart' : 'mdi-heart-outline'"
                    @click="albumData.liked ? dislikeAlbum() : likeAlbum()"
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
                      :objFavorite="albumData.favorite"
                      contentType="album"
                      :objectUUID="$route.params.uuid"
                      @favoriteUpdated="(status) => {
                        albumData.favorite = status
                        isActive.value = false
                      }"
                    />
                    <ReportListItemDialog
                      contentType="album"
                      :objectUUID="$route.params.uuid"
                      @reportSent="isActive.value = false"
                    />
                  </v-list>
                </template>
              </v-menu>
            </div>
          </v-col>
        </v-row>

        <div class="d-flex justify-center justify-md-start align-center mx-5 my-3">
          <router-link
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: albumData.author.profile_url }
            }"
          >
            <v-avatar :size="32">
              <v-img
                v-if="albumData.author.avatar"
                :src="albumData.author.avatar"
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
              params: { profile_url: albumData.author.profile_url }
            }"
            class="text-body-1 text-decoration-none text-black ms-1"
          >
            {{ albumData.author.name }}
          </router-link>
        </div>

        <p
          v-if="albumData.description"
          class="text-body-1 mx-5 my-3"
        >
          {{ albumData.description }}
        </p>

        <div
          v-if="albumData.tags.length > 0"
          class="d-flex flex-wrap ga-2 mx-5"
        >
          <v-btn
            v-for="tag in albumData.tags"
            :key="tag.uuid"
            :to="{
              name: 'TagDetail',
              params: { uuid: tag.uuid },
              query: { tab: 'albums' }
            }"
            prepend-icon="mdi-pound"
            variant="tonal"
            class="text-none"
          >
            {{ tag.name }}
          </v-btn>
        </div>
      </v-sheet>

      <v-row
        dense
        class="my-3"
      >
        <v-col
          :cols="12"
          :lg="7"
        >
          <v-infinite-scroll
            v-if="photoList.length > 0"
            @load="getMorePhotoList"
            mode="intersect"
            empty-text="&nbsp;"
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
                :lg="4"
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
                          query: {
                            from: 'album',
                            album: $route.params.uuid
                          }
                        }"
                        class="d-flex flex-column text-decoration-none text-white w-100 h-100 pa-3"
                      >
                        <h5 class="text-center mb-auto">
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

          <p
            v-else-if="!photoListLoading"
            class="text-body-1 mx-1 my-5"
          >
            {{ $t('portfolio.no_photos') }}
          </p>
        </v-col>
        <v-col
          :cols="12"
          :lg="5"
        >
          <div
            class="overflow-y-auto pa-3"
            style="max-height: 75vh;"
          >
            <CommentList
              contentType="album"
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
