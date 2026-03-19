<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import PortfolioPhotoList from '@/components/auth/PortfolioPhotoList.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n({ useScope: 'global' })

const albumLoading = ref(true)
const albumImageUpdating = ref(false)
const albumUpdating = ref(false)
const albumRemoving = ref(false)

const albumImage = ref(null)
const albumTitle = ref('')
const albumDescription = ref('')
const albumTags = ref([])
const albumCreatedAt = ref(null)
const albumViewCount = ref(0)
const albumLikeCount = ref(0)
const albumRating = ref(0.0)

const albumRemoveDialog = ref(false)

const { getLocaleDateTimeString } = useLocaleDateTime()

const status = ref(null)
const errors = ref(null)

useHead({
  title: () => t('seo_meta.portfolio_album_detail.title')
})

const getAlbumData = async () => {
  try {
    const response = await axios.get(
      '/portfolio/album/author/rud/'
        + route.params.uuid
        +'/'
    )
    albumImage.value = response.data.image
    albumTitle.value = response.data.title
    albumDescription.value = response.data.description
    albumTags.value = response.data.tags
    albumCreatedAt.value = response.data.created_at
    albumViewCount.value = response.data.view_count
    albumLikeCount.value = response.data.like_count
    albumRating.value = response.data.rating
  } catch (error) {
    console.error(error)
  } finally {
    albumLoading.value = false
  }
}

const updateAlbumImage = async (filelist) => {
  albumImageUpdating.value = true

  let formData = new FormData()
  formData.append('image', filelist[0], filelist[0].name)

  try {
    const response = await axios.put(
      '/portfolio/album/author/image-update/'
        + route.params.uuid
        +'/',
      formData
    )
    albumImage.value = response.data.image
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    albumImageUpdating.value = false
  }
}

const updateAlbum = async () => {
  albumUpdating.value = true
  try {
    const response = await axios.put(
      '/portfolio/album/author/rud/'
        + route.params.uuid
        +'/',
      {
        title: albumTitle.value,
        description: albumDescription.value,
        tags: albumTags.value
      }
    )
    if (response.status === 200) {
      router.push({ name: 'PortfolioAlbumList' })
    }
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    albumUpdating.value = false
  }
}

const removeAlbum = async () => {
  albumRemoving.value = true
  try {
    const response = await axios.delete(
      '/portfolio/album/author/rud/'
        + route.params.uuid
        +'/'
    )
    router.push({ name: 'PortfolioAlbumList' })
  } catch (error) {
    console.error(error)
  } finally {
    albumRemoving.value = false
    albumRemoveDialog.value = false
  }
}

onMounted(async () => {
  await getAlbumData()
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
    <router-link
      :to="{ name: 'PortfolioAlbumList' }"
      class="text-h4 text-md-h3 text-primary text-decoration-none"
    >
      {{ $t('portfolio.albums') }}
    </router-link>
    <v-icon
      icon="mdi-chevron-right"
      size="x-large"
    ></v-icon>
  </div>
  <h1 class="text-h4 text-md-h3 d-inline-block">
    {{ albumTitle }}
  </h1>

  <div
    v-if="albumLoading"
    class="d-flex justify-center align-center my-15"
  >
    <v-progress-circular
      indeterminate
      :size="80"
    ></v-progress-circular>
  </div>

  <div v-else>
    <v-sheet
      :elevation="1"
      rounded="lg"
      class="text-center my-5"
    >
      <v-img
        :src="albumImage"
        rounded="t-lg"
      ></v-img>

      <p
        v-if="status === 200"
        class="text-caption text-success"
      >
        {{ $t('portfolio.image_updated_successfully') }}
      </p>
      <div
        v-if="errors?.image"
        class="text-caption text-danger"
      >
        <p v-for="error in errors.image">
          {{ error }}
        </p>
      </div>

      <FileInputButton
        @selectedFiles="updateAlbumImage"
        :loading="albumImageUpdating"
        accept="image/*"
        variant="tonal"
        color="primary"
        class="text-none my-1"
        :text="$t('user.update_cover')"
      ></FileInputButton>
    </v-sheet>

    <v-sheet
      :elevation="1"
      rounded="lg"
      class="my-5 pa-5"
    >
      <v-form @submit.prevent="updateAlbum()">
        <v-text-field
          v-model="albumTitle"
          :readonly="albumUpdating"
          type="text"
          maxlength="128"
          variant="filled"
          :label="$t('portfolio.title')"
          :error-messages="errors?.title ? errors.title : []"
        ></v-text-field>
        <v-textarea
          v-model="albumDescription"
          :readonly="albumUpdating"
          :label="$t('portfolio.description')"
          :error-messages="errors?.description ? errors.description : []"
        ></v-textarea>
        <v-combobox
          v-model="albumTags"
          :readonly="albumUpdating"
          multiple
          chips
          clearable
          :label="$t('portfolio.tags')"
          :error-messages="errors?.tags ? errors.tags : []"
        ></v-combobox>
        <v-btn
          :loading="albumUpdating"
          type="submit"
          variant="flat"
          color="primary"
          size="large"
          block
          class="text-none"
        >
          {{ $t('btn.update') }}
        </v-btn>
      </v-form>

      <v-table
        density="compact"
        class="my-3"
      >
        <tbody>
          <tr>
            <td>{{ $t('portfolio.created_at') }}</td>
            <td>{{ getLocaleDateTimeString(albumCreatedAt) }}</td>
          </tr>
          <tr>
            <td>{{ $t('portfolio.view_count') }}</td>
            <td>{{ albumViewCount }}</td>
          </tr>
          <tr>
            <td>{{ $t('portfolio.likes') }}</td>
            <td>{{ albumLikeCount }}</td>
          </tr>
          <tr>
            <td>{{ $t('portfolio.rating') }}</td>
            <td>{{ albumRating.toFixed(1) }}</td>
          </tr>
        </tbody>
      </v-table>

      <v-btn
        @click="albumRemoveDialog = true"
        variant="outlined"
        size="large"
        block
        class="text-none"
      >
        {{ $t('btn.delete') }}
      </v-btn>
    </v-sheet>
  </div>
  <PortfolioPhotoList />

  <v-dialog
    :model-value="albumRemoveDialog"
    width="auto"
    persistent
  >
    <v-card>
      <v-card-title>
        {{ $t('portfolio.you_want_remove_album') }}
      </v-card-title>
      <v-card-text>
        {{ $t('portfolio.album_information_will_lost') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="albumRemoveDialog = false">
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removeAlbum()"
          :loading="albumRemoving"
        >
          <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
