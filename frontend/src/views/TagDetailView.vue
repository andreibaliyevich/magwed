<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import AlbumList from '@/components/tags/AlbumList.vue'
import ArticleList from '@/components/tags/ArticleList.vue'
import PhotoList from '@/components/tags/PhotoList.vue'
import NotFound from '@/components/NotFound.vue'

const route = useRoute()

const tagLoading = ref(true)
const tagData = ref({
  uuid: '',
  name: ''
})

const errorStatus = ref(null)

const getTagData = async () => {
  try {
    const response = await axios.get(
      '/main/tags/'
        + route.params.uuid
        + '/'
    )
    tagData.value = response.data
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    tagLoading.value = false
  }
}

onMounted(async () => {
  await getTagData()
})
</script>

<template>
  <v-container>
    <div
      v-if="tagLoading"
      class="d-flex justify-center align-center my-15"
    >
      <v-progress-circular
        indeterminate
        :size="80"
      ></v-progress-circular>
    </div>

    <NotFound v-else-if="errorStatus == 404" />

    <div
      v-else
      class="my-5"
    >
      <h1 class="text-h4 text-md-h3 text-center">
        #{{ tagData.name }}
      </h1>

      <div class="text-center my-5">
        <v-btn
          :to="{ query: { tab: 'photos' } }"
          :active="$route.query.tab == 'photos'"
          variant="text"
        >
          {{ $t('portfolio.photos') }}
        </v-btn>
        <v-btn
          :to="{ query: { tab: 'albums' } }"
          :active="$route.query.tab == 'albums'"
          variant="text"
        >
          {{ $t('portfolio.photo_albums') }}
        </v-btn>
        <v-btn
          :to="{ query: { tab: 'articles' } }"
          :active="$route.query.tab == 'articles'"
          variant="text"
        >
          {{ $t('blog.articles') }}
        </v-btn>
      </div>

      <PhotoList
        v-if="$route.query.tab == 'photos'"
        :tagUUID="$route.params.uuid"
      />
      <AlbumList
        v-else-if="$route.query.tab == 'albums'"
        :tagUUID="$route.params.uuid"
      />
      <ArticleList
        v-else-if="$route.query.tab == 'articles'"
        :tagUUID="$route.params.uuid"
      />
    </div>
  </v-container>
</template>
