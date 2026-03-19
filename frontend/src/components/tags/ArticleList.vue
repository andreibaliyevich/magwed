<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const props = defineProps({
  tagUUID: {
    type: String,
    required: true
  }
})

const articleListLoading = ref(true)
const articleList = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const getArticleList = async () => {
  try {
    const response = await axios.get('/blog/article/list/', {
      params: {
        tags: props.tagUUID
      }
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

onMounted(async () => {
  await getArticleList()
})
</script>

<template>
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
