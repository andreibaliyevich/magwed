<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const route = useRoute()
const { t } = useI18n({ useScope: 'global' })

const albumListLoading = ref(true)
const albumList = ref([])
const nextURL = ref(null)

useSeoMeta({
  title: () => t('seo_meta.album_list.title'),
  ogTitle: () => t('seo_meta.album_list.title'),
  description: () => t('seo_meta.album_list.description'),
  ogDescription: () => t('seo_meta.album_list.description'),
  keywords: () => t('seo_meta.album_list.keywords'),
  ogKeywords: () => t('seo_meta.album_list.keywords')
})

const getAlbumList = async () => {
  albumListLoading.value = true
  albumList.value = []

  let params = new URLSearchParams()
  if (route.query.tab === 'popular') {
    params.append('ordering', '-rating')
  } else if (route.query.tab === 'fresh') {
    params.append('ordering', '-created_at')
  } else if (route.query.tab === 'editors') {
    params.append('editors_choice', true)
  } else {
    params.append('ordering', 'rating')
  }

  try {
    const response = await axios.get('/portfolio/album/list/', {
      params: params
    })
    albumList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    albumListLoading.value = false
  }
}

const getMoreAlbumList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      albumList.value = [...albumList.value, ...response.data.results]
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
    if (route.name === 'AlbumList') {
      await getAlbumList()
    }
  }
)

onMounted(async () => {
  await getAlbumList()
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('portfolio.photo_albums') }}
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
        {{ $t('portfolio.popular_albums') }}
      </v-btn>
      <v-btn
        :to="{ query: { tab: 'fresh' } }"
        :active="$route.query.tab === 'fresh'"
        variant="text"
      >
        {{ $t('portfolio.fresh_albums') }}
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
      v-if="albumListLoading"
      class="d-flex justify-center align-center my-15"
    >
      <v-progress-circular
        indeterminate
        :size="80"
      ></v-progress-circular>
    </div>

    <v-infinite-scroll
      v-else-if="albumList.length > 0"
      @load="getMoreAlbumList"
      mode="intersect"
      :empty-text="$t('portfolio.no_more_albums')"
    >
      <v-row
        dense
        class="ma-0"
      >
        <v-col
          v-for="albumItem in albumList"
          :key="albumItem.uuid"
          :cols="12"
          :sm="6"
          :md="4"
          :lg="3"
          :xl="2"
        >
          <v-card rounded="lg">
            <router-link
              :to="{
                name: 'AlbumDetail',
                params: { uuid: albumItem.uuid }
              }"
            >
              <v-img
                :src="albumItem.thumbnail"
                :alt="albumItem.title"
                :aspect-ratio="1/1"
                cover
              ></v-img>
            </router-link>

            <v-card-item>
              <v-card-title>
                <router-link
                  :to="{
                    name: 'AlbumDetail',
                    params: { uuid: albumItem.uuid }
                  }"
                  class="text-decoration-none text-black"
                >
                  {{ albumItem.title }}
                </router-link>
              </v-card-title>

              <router-link
                :to="{
                  name: 'OrganizerDetail',
                  params: { profile_url: albumItem.author.profile_url }
                }"
                class="d-flex align-center text-decoration-none text-black"
              >
                <v-avatar :size="32">
                  <v-img
                    v-if="albumItem.author.avatar"
                    :src="albumItem.author.avatar"
                  ></v-img>
                  <v-icon
                    v-else
                    icon="mdi-account-circle"
                    :size="32"
                    role="img"
                  ></v-icon>
                </v-avatar>
                <div class="text-body-1 ms-1">
                  {{ albumItem.author.name }}
                </div>
              </router-link>

              <v-card-subtitle>
                <div class="d-flex justify-space-between">
                  <span>
                    <v-icon icon="mdi-eye-outline"></v-icon>
                    {{ albumItem.view_count }}
                  </span>
                  <span>
                    <v-icon icon="mdi-heart-outline"></v-icon>
                    {{ albumItem.like_count }}
                  </span>
                  <span>
                    <v-icon icon="mdi-star-outline"></v-icon>
                    {{ albumItem.rating.toFixed(1) }}
                  </span>
                </div>
              </v-card-subtitle>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
    </v-infinite-scroll>

    <v-alert
      v-else
      type="info"
      variant="tonal"
      class="my-5"
    >
      {{ $t('portfolio.no_albums') }}
    </v-alert>
  </v-container>
</template>
