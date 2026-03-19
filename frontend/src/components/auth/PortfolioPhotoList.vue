<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import { ref, computed, watch, onMounted } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const route = useRoute()

const photoListLoading = ref(true)
const photoList = ref([])
const nextURL = ref(null)

const photosUploadStatus = ref(0)
const photoProcessing = ref(false)

const photoUuid = ref(null)
const photoImage = ref(null)
const photoDevice = ref('')
const photoFNumber = ref(null)
const photoExposureTime = ref('')
const photoFocalLength = ref(null)
const photoPhotographicSensitivity = ref(null)
const photoTitle = ref('')
const photoDescription = ref('')
const photoTags = ref([])
const photoUploadedAt = ref(null)
const photoViewCount = ref(0)
const photoLikeCount = ref(0)
const photoRating = ref(0.0)

const { getLocaleDateTimeString } = useLocaleDateTime()

const uploadPhotosDialog = ref(false)
const photoUpdateDialog = ref(false)
const photoRemoveDialog = ref(false)

const errors = ref(null)

const photoIndex = computed(() => {
  return photoList.value.findIndex((element) => {
    return element.uuid === photoUuid.value
  })
})

const photosUploadStatusRound = computed(() => {
  return Math.round(photosUploadStatus.value)
})

const getPhotoList = async () => {
  let params = new URLSearchParams()
  if (route.params.uuid) {
    params.append('album', route.params.uuid)
  } else {
    params.append('album_is_null', true)
  }

  try {
    const response = await axios.get('/portfolio/photo/author/list-create/', {
      params: params
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

const uploadPhotos = async (filelist) => {
  photosUploadStatus.value = 0
  uploadPhotosDialog.value = true
  const uploadStep = 100 / filelist.length

  for (let i = 0; i < filelist.length; i++) {
    if (uploadPhotosDialog.value) {
      let formData = new FormData()
      if (route.params.uuid) {
        formData.append('album', route.params.uuid)
      }
      formData.append('image', filelist[i], filelist[i].name)

      try {
        const response = await axios.post(
          '/portfolio/photo/author/list-create/',
          formData
        )
        photoList.value.unshift(response.data)
        photosUploadStatus.value += uploadStep
      } catch (error) {
        console.error(error)
      }
    } else {
      break
    }
  }
  uploadPhotosDialog.value = false
}

const getPhotoData = async (pUuid) => {
  try {
    const response = await axios.get(
      '/portfolio/photo/author/rud/'
        + pUuid
        +'/'
    )
    photoUuid.value = pUuid
    photoImage.value = response.data.image

    photoDevice.value = response.data.device
    photoFNumber.value = response.data.f_number
    photoExposureTime.value = response.data.exposure_time
    photoFocalLength.value = response.data.focal_length
    photoPhotographicSensitivity.value = response.data.photographic_sensitivity

    photoTitle.value = response.data.title
    photoDescription.value = response.data.description
    photoTags.value = response.data.tags

    photoUploadedAt.value = response.data.uploaded_at
    photoViewCount.value = response.data.view_count
    photoLikeCount.value = response.data.like_count
    photoRating.value = response.data.rating
  } catch (error) {
    console.error(error)
  }
}

const updatePhoto = async () => {
  photoProcessing.value = true

  if (!photoFNumber.value) {
    photoFNumber.value = null
  }
  if (!photoFocalLength.value) {
    photoFocalLength.value = null
  }
  if (!photoPhotographicSensitivity.value) {
    photoPhotographicSensitivity.value = null
  }

  try {
    const response = await axios.put(
      '/portfolio/photo/author/rud/'
        + photoUuid.value
        +'/',
      {
        device: photoDevice.value,
        f_number: photoFNumber.value,
        exposure_time: photoExposureTime.value,
        focal_length: photoFocalLength.value,
        photographic_sensitivity: photoPhotographicSensitivity.value,
        title: photoTitle.value,
        description: photoDescription.value,
        tags: photoTags.value
      }
    )
    photoList.value[photoIndex.value].title = photoTitle.value
  } catch (error) {
    errors.value = error.response.data
  } finally {
    photoProcessing.value = false
  }
}

const removePhoto = async () => {
  photoProcessing.value = true
  try {
    const response = await axios.delete(
      '/portfolio/photo/author/rud/'
        + photoUuid.value
        +'/'
    )
    if (response.status === 204) {
      photoList.value = photoList.value.filter((element) => {
        return element.uuid !== photoUuid.value
      })
    }
  } catch (error) {
    console.error(error)
  } finally {
    photoUuid.value = null
    photoProcessing.value = false
    photoRemoveDialog.value = false
  }
}

watch(photoIndex, async (newValue) => {
  if (newValue === photoList.value.length - 1 && nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      photoList.value = [...photoList.value, ...response.data.results]
      nextURL.value = response.data.next
    } catch (error) {
      console.error(error)
    }
  }
})

onMounted(async () => {
  await getPhotoList()
})
</script>

<template>
  <div class="my-5">
    <FileDropZoneInputButton
      @selectedFiles="uploadPhotos"
      :zoneText="$t('portfolio.drag_and_drop_image')"
      :buttonText="$t('portfolio.upload_photos')"
      accept="image/*"
      multiple
    ></FileDropZoneInputButton>

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
                content-class="d-flex flex-column text-white text-center w-100 h-100 pa-3"
              >
                <h5>{{ photoItem.title }}</h5>
                <div class="my-auto">
                  <v-btn
                    @click="() => {
                      photoUpdateDialog = true
                      getPhotoData(photoItem.uuid)
                    }"
                    icon="mdi-pencil"
                    variant="flat"
                    color="grey-lighten-3"
                    size="x-small"
                  ></v-btn>
                  <v-btn
                    @click="() => {
                      photoUuid = photoItem.uuid
                      photoRemoveDialog = true
                    }"
                    icon="mdi-delete"
                    variant="flat"
                    color="red-darken-3"
                    size="x-small"
                    class="ms-1"
                  ></v-btn>
                </div>
                <small>{{ getLocaleDateTimeString(photoItem.uploaded_at) }}</small>
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
  </div>

  <v-dialog
    :model-value="uploadPhotosDialog"
    :width="500"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('portfolio.uploading_photos') }}
      </v-card-title>
      <div class="px-3">
        <v-progress-linear
          :model-value="photosUploadStatusRound"
          :height="16"
          rounded
          striped
          color="blue"
        >
          <strong>{{ photosUploadStatusRound }}%</strong>
        </v-progress-linear>
      </div>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="uploadPhotosDialog = false">
          {{ $t('btn.cancel') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="photoUpdateDialog"
    width="80%"
    persistent
  >
    <v-card rounded="lg">
      <div class="overflow-y-auto">
        <v-hover v-slot="{ isHovering, props }">
          <v-sheet
            v-bind="props"
            position="relative"
          >
            <v-img
              :src="photoImage"
              :alt="photoTitle"
              max-width="100%"
              max-height="75vh"
            ></v-img>
            <v-overlay
              :model-value="isHovering"
              contained
              :opacity="0"
              content-class="d-flex justify-space-between align-center w-100 h-100 pa-3"
            >
              <v-btn
                @click="getPhotoData(photoList[photoIndex - 1].uuid)"
                :disabled="photoIndex === 0"
                icon="mdi-chevron-left"
                :elevation="1"
              ></v-btn>
              <v-btn
                @click="getPhotoData(photoList[photoIndex + 1].uuid)"
                :disabled="photoIndex === photoList.length - 1"
                icon="mdi-chevron-right"
                :elevation="1"
              ></v-btn>
            </v-overlay>
          </v-sheet>
        </v-hover>

        <v-row
          dense
          class="mx-1 mx-sm-5 mx-md-10 mx-lg-16 my-3"
        >
          <v-col
            :cols="12"
            :md="12"
          >
            <v-text-field
              v-model="photoTitle"
              :readonly="photoProcessing"
              type="text"
              maxlength="128"
              variant="filled"
              :label="$t('portfolio.title')"
              :error-messages="errors?.title ? errors.title : []"
            ></v-text-field>
          </v-col>
          <v-col
            :cols="12"
            :md="12"
          >
            <v-textarea
              v-model="photoDescription"
              :readonly="photoProcessing"
              :label="$t('portfolio.description')"
              :error-messages="errors?.description ? errors.description : []"
            ></v-textarea>
          </v-col>
          <v-col
            :cols="12"
            :md="12"
          >
            <v-text-field
              v-model="photoDevice"
              :readonly="photoProcessing"
              type="text"
              maxlength="128"
              variant="filled"
              :label="$t('portfolio.device')"
              :error-messages="errors?.device ? errors.device : []"
            ></v-text-field>
          </v-col>
          <v-col
            :cols="12"
            :md="6"
          >
            <v-text-field
              v-model="photoFNumber"
              :readonly="photoProcessing"
              type="number"
              step="0.01"
              variant="filled"
              :label="$t('portfolio.f_number')"
              :error-messages="errors?.f_number ? errors.f_number : []"
            ></v-text-field>
          </v-col>
          <v-col
            :cols="12"
            :md="6"
          >
            <v-text-field
              v-model="photoExposureTime"
              :readonly="photoProcessing"
              type="text"
              maxlength="32"
              variant="filled"
              :label="$t('portfolio.exposure_time')"
              :error-messages="errors?.exposure_time ? errors.exposure_time : []"
            ></v-text-field>
          </v-col>
          <v-col
            :cols="12"
            :md="6"
          >
            <v-text-field
              v-model="photoFocalLength"
              :readonly="photoProcessing"
              type="number"
              step="0.01"
              variant="filled"
              :label="$t('portfolio.focal_length')"
              :error-messages="errors?.focal_length ? errors.focal_length : []"
            ></v-text-field>
          </v-col>
          <v-col
            :cols="12"
            :md="6"
          >
            <v-text-field
              v-model="photoPhotographicSensitivity"
              :readonly="photoProcessing"
              type="number"
              min="0"
              variant="filled"
              :label="$t('portfolio.photographic_sensitivity')"
              :error-messages="
                errors?.photographic_sensitivity
                  ? errors.photographic_sensitivity
                  : []
              "
            ></v-text-field>
          </v-col>
          <v-col
            :cols="12"
            :md="12"
          >
            <v-combobox
              v-model="photoTags"
              :readonly="photoProcessing"
              multiple
              chips
              clearable
              :label="$t('portfolio.tags')"
              :error-messages="errors?.tags ? errors.tags : []"
            ></v-combobox>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-table
          density="compact"
          class="mx-1 mx-sm-5 mx-md-10 mx-lg-16 my-3"
        >
          <tbody>
            <tr>
              <td>{{ $t('portfolio.uploaded_at') }}</td>
              <td>{{ getLocaleDateTimeString(photoUploadedAt) }}</td>
            </tr>
            <tr>
              <td>{{ $t('portfolio.view_count') }}</td>
              <td>{{ photoViewCount }}</td>
            </tr>
            <tr>
              <td>{{ $t('portfolio.likes') }}</td>
              <td>{{ photoLikeCount }}</td>
            </tr>
            <tr>
              <td>{{ $t('portfolio.rating') }}</td>
              <td>{{ photoRating.toFixed(1) }}</td>
            </tr>
          </tbody>
        </v-table>
      </div>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            photoUpdateDialog = false
            photoUuid = null
            photoImage = null
            photoDevice = ''
            photoFNumber = null
            photoExposureTime = ''
            photoFocalLength = null
            photoPhotographicSensitivity = null
            photoTitle = ''
            photoDescription = ''
            photoTags = []
            photoUploadedAt = null
            photoViewCount = 0
            photoLikeCount = 0
            photoRating = 0.0
            errors = null
          }"
        >
          {{ $t('btn.close') }}
        </v-btn>
        <v-btn
          @click="updatePhoto()"
          :loading="photoProcessing"
          :disabled="!photoUuid"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.update') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="photoRemoveDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('portfolio.you_want_remove_photo') }}
      </v-card-title>
      <v-card-text>
        {{ $t('portfolio.photo_information_will_lost') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            photoUuid = null
            photoRemoveDialog = false
          }"
        >
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removePhoto()"
          :loading="photoProcessing"
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
