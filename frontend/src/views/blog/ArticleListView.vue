<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const route = useRoute()
const { t, locale } = useI18n({ useScope: 'global' })

const articleListLoading = ref(true)
const articleList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

useSeoMeta({
  title: () => t('seo_meta.article_list.title'),
  ogTitle: () => t('seo_meta.article_list.title'),
  description: () => t('seo_meta.article_list.description'),
  ogDescription: () => t('seo_meta.article_list.description'),
  keywords: () => t('seo_meta.article_list.keywords'),
  ogKeywords: () => t('seo_meta.article_list.keywords')
})

const getArticleList = async () => {
  articleListLoading.value = true
  articleList.value = []

  let params = new URLSearchParams()
  if (route.query.author) {
    params.append('author', route.query.author)
  }
  if (route.query.category) {
    params.append('categories', route.query.category)
  }
  if (route.query.year) {
    params.append('published_at_year', route.query.year)
  }

  try {
    const response = await axios.get('/blog/article/list/', {
      params: params
    })
    articleList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    articleListLoading.value = false
  }
}

const getMoreArticleList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      articleList.value = [...articleList.value, ...response.data.results]
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
  await getArticleList()
})

watch(
  () => route.query,
  async () => {
    if (route.name === 'ArticleList') {
      await getArticleList()
    }
  }
)

onMounted(async () => {
  await getArticleList()
})
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center my-5">
    {{ $t('blog.articles') }}
  </h1>

  <div
    v-if="articleListLoading"
    class="d-flex justify-center align-center my-15"
  >
    <v-progress-circular
      indeterminate
      :size="80"
    ></v-progress-circular>
  </div>

  <v-infinite-scroll
    v-else-if="articleList.length > 0"
    @load="getMoreArticleList"
    mode="intersect"
    :empty-text="$t('blog.no_more_articles')"
  >
    <div
      v-for="article in articleList"
      :key="article.slug"
      class="mx-1 my-1"
    >
      <v-card rounded="lg">
        <router-link
          :to="{
            name: 'ArticleDetail',
            params: {
              locale: $i18n.locale,
              slug: article.slug
            }
          }"
          class="text-black text-decoration-none"
        >
          <v-img
            :src="article.thumbnail"
            :height="200"
            cover
            class="align-end text-white"
          >
            <v-card-title>{{ article.translated_title }}</v-card-title>
          </v-img>
        </router-link>
        <v-card-subtitle>
          <div class="d-flex flex-wrap ga-1 py-2">
            <v-chip
              v-for="categoryValue in article.categories"
              :key="`${article.slug}-category-${categoryValue}`"
              density="compact"
            >
              {{ $t(`category_choices.${categoryValue}`) }}
            </v-chip>
          </div>
          <v-icon
            icon="mdi-calendar-month-outline"
            size="default"
          ></v-icon>
          {{ getLocaleDateString(article.published_at) }}
        </v-card-subtitle>
        <v-card-text>
          {{ article.translated_description }}
        </v-card-text>
      </v-card>
    </div>
  </v-infinite-scroll>

  <v-alert
    v-else
    type="info"
    variant="tonal"
    class="my-5"
  >
    {{ $t('blog.no_articles') }}
  </v-alert>
</template>
