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
const { locale } = useI18n({ useScope: 'global' })
const userStore = useUserStore()

const articleLoading = ref(true)
const articleData = ref({
  uuid: '',
  author: {
    uuid: '',
    name: ''
  },
  categories: [],
  translated_title: '',
  image: null,
  translated_description: '',
  translated_content: '',
  tags: [],
  published_at: null,
  view_count: 0,
  favorite: null
})

const { getLocaleDateString } = useLocaleDateTime()

const upViewCountTimeout = ref(null)
const errorStatus = ref(null)

useSeoMeta({
  title: () => articleData.value.translated_title,
  ogTitle: () => articleData.value.translated_title,
  description: () => articleData.value.translated_description,
  ogDescription: () => articleData.value.translated_description
})

const upArticleViewCount = async () => {
  try {
    const response = await axios.post(
      '/blog/article/up-view-count/'
        + route.params.slug
        + '/'
    )
    articleData.value.view_count += 1
  } catch (error) {
    console.error(error)
  }
}

const getArticleData = async () => {
  articleLoading.value = true
  try {
    const response = await axios.get(
      '/blog/article/retrieve/'
        + route.params.slug
        + '/'
    )
    articleData.value = response.data
    upViewCountTimeout.value = setTimeout(upArticleViewCount, 3000)
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    articleLoading.value = false
  }
}

watch(locale, async () => {
  await getArticleData()
})

watch(
  () => route.params.slug,
  async () => {
    if (route.name === 'ArticleDetail') {
      errorStatus.value = null
      await getArticleData()
    }
  }
)

onMounted(async () => {
  await getArticleData()
})

onUnmounted(() => {
  clearTimeout(upViewCountTimeout.value)
})
</script>

<template>
  <div
    v-if="articleLoading"
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
    <v-img
      :src="articleData.image"
      :height="300"
      cover
      rounded="lg"
    ></v-img>
    <h1 class="text-h4 text-md-h3 my-5">{{ articleData.translated_title }}</h1>

    <div class="d-flex flex-wrap ga-1">
      <v-chip
        v-for="categoryValue in articleData.categories"
        :key="categoryValue"
      >
        {{ $t(`category_choices.${categoryValue}`) }}
      </v-chip>

      <v-menu
        v-if="userStore.isLoggedIn"
        location="start"
        :close-on-content-click="false"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            icon="mdi-dots-horizontal"
            variant="text"
            class="ms-auto"
          ></v-btn>
        </template>
        <template v-slot:default="{ isActive }">
          <v-list density="compact">
            <FavoriteListItem
              :objFavorite="articleData.favorite"
              contentType="article"
              :objectUUID="articleData.uuid"
              @favoriteUpdated="(status) => {
                articleData.favorite = status
                isActive.value = false
              }"
            />
            <ReportListItemDialog
              contentType="article"
              :objectUUID="articleData.uuid"
              @reportSent="isActive.value = false"
            />
          </v-list>
        </template>
      </v-menu>
    </div>

    <div class="d-flex flex-wrap ga-5 mb-5">
      <div class="d-flex align-center">
        <span class="text-secondary">
          {{ $t('blog.author') }}:
        </span>
        <router-link
          :to="{
            name: 'ArticleList',
            query: { author: articleData.author.uuid }
          }"
          class="text-decoration-none text-grey-darken-4 ms-1"
        >
          {{ articleData.author.name }}
        </router-link>
      </div>
      <div class="d-flex align-center text-secondary">
        <v-icon
          icon="mdi-calendar-month-outline"
          :size="24"
          class="me-1"
        ></v-icon>
        {{ getLocaleDateString(articleData.published_at) }}
      </div>
      <div class="d-flex align-center text-secondary">
        <v-icon
          icon="mdi-eye-outline"
          :size="24"
          class="me-1"
        ></v-icon>
        {{ articleData.view_count }}
      </div>
    </div>

    <div v-html="articleData.translated_content"></div>

    <div
      v-if="articleData.tags.length > 0"
      class="d-flex flex-wrap my-5"
    >
      <v-btn
        v-for="tag in articleData.tags"
        :key="tag.uuid"
        :to="{
          name: 'TagDetail',
          params: { uuid: tag.uuid },
          query: { tab: 'articles' }
        }"
        prepend-icon="mdi-pound"
        variant="tonal"
        class="text-none ma-1"
      >
        {{ tag.name }}
      </v-btn>
    </div>

    <CommentList
      contentType="article"
      :objectUUID="articleData.uuid"
    />
  </div>
</template>
