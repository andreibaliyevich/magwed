<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const route = useRoute()
const { t, locale } = useI18n({ useScope: 'global' })

const favoriteListLoading = ref(false)
const favoriteList = ref([])
const favoriteCount = ref(0)
const nextURL = ref(null)

useHead({
  title: () => t('seo_meta.favorites.title')
})

const getFavoriteList = async () => {
  favoriteListLoading.value = true

  let params = new URLSearchParams()
  if (route.query.type) {
    params.append('content_type__model', route.query.type)
  }

  try {
    const response = await axios.get('/social/favorite/list/', {
      params: params
    })
    favoriteList.value = response.data.results
    favoriteCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    favoriteListLoading.value = false
  }
}

const getMoreFavoriteList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      favoriteList.value = [...favoriteList.value, ...response.data.results]
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

watch(locale, async () => {
  await getFavoriteList()
})

watch(
  () => route.query.type,
  async () => {
    if (route.name === 'Favorites') {
      await getFavoriteList()
    }
  }
)

onMounted(async () => {
  await getFavoriteList()
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('favorites.favorites') }} ({{ favoriteCount }})
    </h1>

    <div class="text-center mb-5">
      <v-btn
        :to="{ name: 'Favorites' }"
        :active="!$route.query.type"
        variant="text"
      >
        {{ $t('favorites.all') }}
      </v-btn>
      <v-btn
        :to="{ query: { type: 'photo' } }"
        :active="$route.query.type === 'photo'"
        variant="text"
      >
        {{ $t('favorites.photos') }}
      </v-btn>
      <v-btn
        :to="{ query: { type: 'album' } }"
        :active="$route.query.type === 'album'"
        variant="text"
      >
        {{ $t('favorites.albums') }}
      </v-btn>
      <v-btn
        :to="{ query: { type: 'article' } }"
        :active="$route.query.type === 'article'"
        variant="text"
      >
        {{ $t('favorites.articles') }}
      </v-btn>
    </div>

    <div
      v-if="favoriteListLoading"
      class="d-flex justify-center align-center my-15"
    >
      <v-progress-circular
        indeterminate
        :size="80"
      ></v-progress-circular>
    </div>

    <v-infinite-scroll
      v-else-if="favoriteList.length > 0"
      @load="getMoreFavoriteList"
      mode="intersect"
      empty-text="&nbsp;"
    >
      <v-row
        dense
        class="ma-0"
      >
        <v-col
          v-for="favorite in favoriteList"
          :key="favorite.uuid"
          :cols="12"
          :sm="6"
          :md="4"
          :lg="3"
          :xl="2"
        >
          <v-card
            v-if="favorite.content_type_model === 'photo'"
            rounded="lg"
          >
            <router-link
              :to="{
                name: 'PhotoDetail',
                params: { uuid: favorite.content_object.uuid }
              }"
            >
              <v-img
                :src="favorite.content_object.thumbnail"
                :alt="favorite.content_object.title"
                :aspect-ratio="1/1"
                cover
              ></v-img>
            </router-link>
            <v-card-item>
              <v-card-title class="text-center">
                <router-link
                  :to="{
                    name: 'PhotoDetail',
                    params: { uuid: favorite.content_object.uuid }
                  }"
                  class="text-decoration-none text-black"
                >
                  <v-icon icon="mdi-image-outline"></v-icon>
                  {{ favorite.content_object.title }}
                </router-link>
              </v-card-title>
            </v-card-item>
          </v-card>

          <v-card
            v-else-if="favorite.content_type_model === 'album'"
            rounded="lg"
          >
            <router-link
              :to="{
                name: 'AlbumDetail',
                params: { uuid: favorite.content_object.uuid }
              }"
            >
              <v-img
                :src="favorite.content_object.thumbnail"
                :alt="favorite.content_object.title"
                :aspect-ratio="1/1"
                cover
              ></v-img>
            </router-link>
            <v-card-item>
              <v-card-title class="text-center">
                <router-link
                  :to="{
                    name: 'AlbumDetail',
                    params: { uuid: favorite.content_object.uuid }
                  }"
                  class="text-decoration-none text-black"
                >
                  <v-icon icon="mdi-image-multiple-outline"></v-icon>
                  {{ favorite.content_object.title }}
                </router-link>
              </v-card-title>
            </v-card-item>
          </v-card>

          <v-card
            v-else-if="favorite.content_type_model === 'article'"
            rounded="lg"
          >
            <router-link
              :to="{
                name: 'ArticleDetail',
                params: { slug: favorite.content_object.slug }
              }"
            >
              <v-img
                :src="favorite.content_object.thumbnail"
                :alt="favorite.content_object.translated_title"
                :aspect-ratio="1/1"
                cover
              ></v-img>
            </router-link>
            <v-card-item>
              <v-card-title class="text-center">
                <router-link
                  :to="{
                    name: 'ArticleDetail',
                    params: { slug: favorite.content_object.slug }
                  }"
                  class="text-decoration-none text-black"
                >
                  <v-icon icon="mdi-newspaper-variant-outline"></v-icon>
                  {{ favorite.content_object.translated_title }}
                </router-link>
              </v-card-title>
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
      {{ $t('favorites.no_favorites') }}
    </v-alert>
  </v-container>
</template>
