<script setup>
import axios from 'axios'
import 'cropperjs/dist/cropper.css'
import Cropper from 'cropperjs'
import { ref, onMounted } from 'vue'

const coverLoading = ref(true)
const coverProcessing = ref(false)

const cover = ref(null)

const coverUpdateDialog = ref(false)
const coverRemoveDialog = ref(false)

const coverImgLoading = ref(false)
const coverImg = ref(null)
const coverCropper = ref(null)

const status = ref(null)
const errors = ref(null)

const getCover = async () => {
  try {
    const response = await axios.get('/accounts/auth/cover/')
    cover.value = response.data.cover
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    coverLoading.value = false
  }
}

const loadCoverImg = async (filelist) => {
  coverImgLoading.value = true
  coverUpdateDialog.value = true

  const reader = new FileReader()
  reader.readAsDataURL(filelist[0])

  reader.onload = () => {
    coverImg.value.src = reader.result
    coverImg.value.alt = filelist[0].name

    coverCropper.value = new Cropper(coverImg.value, {
      viewMode: 1,
      dragMode: 'crop',
      aspectRatio: 3 / 1,
      zoomable: false,
      ready() {
        coverImgLoading.value = false
      }
    })
  }
}

const updateCover = async (filelist) => {
  coverProcessing.value = true

  const croppedCanvas = coverCropper.value.getCroppedCanvas({
    width: 1500,
    height: 500
  })
  const canvasBlob = await new Promise((resolve) => {
    croppedCanvas.toBlob((blob) => {
      resolve(blob)
    })
  })

  let formData = new FormData()
  formData.append('cover', canvasBlob, coverImg.value.alt)

  try {
    const response = await axios.put('/accounts/auth/cover/', formData)
    cover.value = response.data.cover
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    coverProcessing.value = false
    coverUpdateDialog.value = false
    coverCropper.value.destroy()
    coverCropper.value = null
  }
}

const removeCover = async () => {
  coverProcessing.value = true
  try {
    const response = await axios.delete('/accounts/auth/cover/')
    cover.value = null
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    coverProcessing.value = false
    coverRemoveDialog.value = false
  }
}

onMounted(async () => {
  await getCover()
})
</script>

<template>
  <v-card
    rounded="lg"
    class="my-5"
  >
    <div
      v-if="coverLoading"
      class="d-flex justify-center align-center my-10"
    >
      <v-progress-circular indeterminate></v-progress-circular>
      &nbsp;
      {{ $t('user.loading_cover') }}
    </div>
    <div
      v-else
      class="text-center"
    >
      <v-img
        :src="cover ? cover : '/cover.jpg'"
        :aspect-ratio="3/1"
        cover
      ></v-img>

      <small
        v-if="status === 200"
        class="text-success"
      >
        {{ $t('user.cover_updated_successfully') }}
      </small>
      <small
        v-else-if="status === 204"
        class="text-success"
      >
        {{ $t('user.cover_removed_successfully') }}
      </small>
      <div
        v-if="errors?.cover"
        class="text-danger"
      >
        <small v-for="error in errors.cover">
          {{ error }}
        </small>
      </div>

      <v-card-actions class="d-flex justify-space-evenly">
        <FileInputButton
          @selectedFiles="loadCoverImg"
          accept="image/*"
          variant="flat"
          color="primary"
          class="text-none"
          :text="$t('user.update_cover')"
        ></FileInputButton>
        <v-btn
          @click="coverRemoveDialog = true"
          :disabled="!cover"
          variant="outlined"
          class="text-none"
        >
          {{ $t('user.remove_cover') }}
        </v-btn>
      </v-card-actions>

      <small class="text-secondary">
        {{ $t('form_help.input_img', { width: '1500', height: '500' }) }}
      </small>
    </div>
  </v-card>

  <v-dialog
    :model-value="coverUpdateDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <div class="d-flex justify-center align-center">
        <img
          ref="coverImg"
          src="/loading.gif"
          alt="loading"
          style="
            max-width: 100%;
            max-height: 75vh;
          "
        >
      </div>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            coverUpdateDialog = false
            coverCropper.destroy()
            coverCropper = null
          }"
          :disabled="coverImgLoading"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="updateCover()"
          :loading="coverProcessing"
          :disabled="coverImgLoading"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.update') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="coverRemoveDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('user.you_want_remove_cover') }}
      </v-card-title>
      <v-card-text>
        {{ $t('user.cover_will_be_set_default') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="coverRemoveDialog = false">
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removeCover()"
          :loading="coverProcessing"
        >
          <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
