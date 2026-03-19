<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const router = useRouter()
const { t, locale } = useI18n({ useScope: 'global' })

const albumListLoading = ref(true)
const albumList = ref([])
const nextURL = ref(null)

const albumProcessing = ref(false)
const albumUuid = ref(null)
const albumImage = ref(null)
const albumTitle = ref('')
const albumDescription = ref('')

const albumCreateDialog = ref(false)
const albumRemoveDialog = ref(false)

const albumImg = ref(null)

const { getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)

useHead({
  title: () => t('seo_meta.portfolio_album_list.title')
})

const getAlbumList = async () => {
  try {
    const response = await axios.get('/portfolio/album/author/list-create/')
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

const loadAlbumImg = async (filelist) => {
  albumImage.value = filelist[0]
  const reader = new FileReader()
  reader.readAsDataURL(filelist[0])
  reader.onload = () => {
    albumImg.value.src = reader.result
    albumImg.value.alt = filelist[0].name
  }
}

const createAlbum = async () => {
  albumProcessing.value = true
  try {
    let formData = new FormData()
    formData.append('image', albumImage.value, albumImage.value.name)
    formData.append('title', albumTitle.value)
    formData.append('description', albumDescription.value)

    const response = await axios.post(
      '/portfolio/album/author/list-create/',
      formData
    )
    albumCreateDialog.value = false
    router.push({
      name: 'PortfolioAlbumDetail',
      params: {
        locale: locale.value,
        uuid: response.data.uuid
      }
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    albumProcessing.value = false
  }
}

const removeAlbum = async () => {
  albumProcessing.value = true
  try {
    const response = await axios.delete(
      '/portfolio/album/author/rud/'
        + albumUuid.value
        +'/'
    )
    albumList.value = albumList.value.filter((element) => {
      return element.uuid !== albumUuid.value
    })
  } catch (error) {
    console.error(error)
  } finally {
    albumUuid.value = null
    albumProcessing.value = false
    albumRemoveDialog.value = false
  }
}

onMounted(async () => {
  await getAlbumList()
})
</script>

<template>
  <div class="d-flex align-center my-5">
    <router-link
      :to="{ name: 'Portfolio' }"
      class="text-h4 text-md-h3 text-primary text-decoration-none"
    >
      {{ $t('portfolio.portfolio') }}
    </router-link>
    <v-icon
      icon="mdi-chevron-right"
      size="x-large"
    ></v-icon>
    <h1 class="text-h4 text-md-h3">
      {{ $t('portfolio.albums') }}
    </h1>
  </div>

  <v-btn
    @click="albumCreateDialog = true"
    variant="tonal"
    color="primary"
    block
    class="text-none"
    append-icon="mdi-plus-circle-outline"
  >
    {{ $t('portfolio.create_album') }}
  </v-btn>

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
    empty-text="&nbsp;"
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
        :lg="4"
      >
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            rounded="lg"
          >
            <v-img
              :src="albumItem.thumbnail"
              :alt="albumItem.title"
              :aspect-ratio="1/1"
              cover
            ></v-img>
            <v-card-item>
              <v-card-title>{{ albumItem.title }}</v-card-title>
              <v-card-subtitle>
                {{ getLocaleDateTimeString(albumItem.created_at) }}
              </v-card-subtitle>
            </v-card-item>
            <v-overlay
              :model-value="isHovering"
              contained
              scrim="black"
              :opacity="0.5"
              content-class="d-flex justify-center align-center w-100 h-100"
            >
              <v-btn
                :to="{
                  name: 'PortfolioAlbumDetail',
                  params: { uuid: albumItem.uuid }
                }"
                icon="mdi-pencil"
                variant="flat"
                color="grey-lighten-3"
                size="x-small"
              ></v-btn>
              <v-btn
                @click="() => {
                  albumUuid = albumItem.uuid
                  albumRemoveDialog = true
                }"
                icon="mdi-delete"
                variant="flat"
                color="red-darken-3"
                size="x-small"
                class="ms-1"
              ></v-btn>
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
    {{ $t('portfolio.no_albums') }}
  </v-alert>

  <v-dialog
    v-model="albumCreateDialog"
    :width="500"
    persistent
  >
    <v-card
      :title="$t('portfolio.creating_album')"
      rounded="lg"
    >
      <div class="overflow-y-auto pa-5">
        <div class="d-flex justify-center align-center">
          <img
            ref="albumImg"
            src="/placeholder.svg"
            alt="placeholder"
            style="max-width: 100%; max-height: 75vh;"
          >
        </div>
        <FileInputButton
          @selectedFiles="loadAlbumImg"
          accept="image/*"
          variant="flat"
          color="primary"
          block
          class="text-none mb-5"
          :text="$t('portfolio.choose_image')"
        ></FileInputButton>

        <v-text-field
          v-model="albumTitle"
          :readonly="albumProcessing"
          type="text"
          maxlength="128"
          variant="filled"
          :label="$t('portfolio.title')"
          :error-messages="errors?.title ? errors.title : []"
        ></v-text-field>
        <v-textarea
          v-model="albumDescription"
          :readonly="albumProcessing"
          :label="$t('portfolio.description')"
          :error-messages="errors?.description ? errors.description : []"
        ></v-textarea>
      </div>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            albumCreateDialog = false
            albumImage = null
            albumTitle = ''
            albumDescription = ''
            errors = null
          }"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="createAlbum()"
          :loading="albumProcessing"
          :disabled="!albumImage || !albumTitle"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.create') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="albumRemoveDialog"
    :width="500"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('portfolio.you_want_remove_album') }}
      </v-card-title>
      <v-card-text>
        {{ $t('portfolio.album_information_will_lost') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            albumUuid = null
            albumRemoveDialog = false
          }"
        >
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removeAlbum()"
          :loading="albumProcessing"
        >
          <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 0.3em;
}
</style>
