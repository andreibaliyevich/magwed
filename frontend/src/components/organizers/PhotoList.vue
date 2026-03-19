<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const getPhotoList = async () => {
  try {
    const response = await axios.get('/portfolio/photo/list/', {
      params: {
        author: props.userUUID,
        album_is_null: true
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

onMounted(async () => {
  await getPhotoList()
})
</script>

<template>
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
                  query: {
                    from: 'author',
                    author: userUUID
                  }
                }"
                class="d-flex flex-column text-decoration-none text-white w-100 h-100 pa-3"
              >
                <h5 class="text-h6 text-center mb-auto">
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
                    {{ photoItem.rating }}
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
</template>
