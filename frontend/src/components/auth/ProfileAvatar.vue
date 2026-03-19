<script setup>
import axios from 'axios'
import 'cropperjs/dist/cropper.css'
import Cropper from 'cropperjs'
import { ref } from 'vue'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()

const avatarProcessing = ref(false)

const avatarUpdateDialog = ref(false)
const avatarRemoveDialog = ref(false)

const avatarImgLoading = ref(false)
const avatarImg = ref(null)
const avatarCropper = ref(null)

const status = ref(null)
const errors = ref(null)

const loadAvatarImg = async (filelist) => {
  avatarImgLoading.value = true
  avatarUpdateDialog.value = true

  const reader = new FileReader()
  reader.readAsDataURL(filelist[0])

  reader.onload = () => {
    avatarImg.value.src = reader.result
    avatarImg.value.alt = filelist[0].name

    avatarCropper.value = new Cropper(avatarImg.value, {
      viewMode: 1,
      dragMode: 'crop',
      aspectRatio: 1 / 1,
      zoomable: false,
      ready() {
        avatarImgLoading.value = false
      }
    })
  }
}

const updateAvatar = async () => {
  avatarProcessing.value = true

  const croppedCanvas = avatarCropper.value.getCroppedCanvas({
    width: 500,
    height: 500
  })
  const canvasBlob = await new Promise((resolve) => {
    croppedCanvas.toBlob((blob) => {
      resolve(blob)
    })
  })

  let formData = new FormData()
  formData.append('avatar', canvasBlob, avatarImg.value.alt)

  try {
    const response = await axios.put('/accounts/auth/avatar/', formData)
    userStore.updateAvatar(response.data.avatar)
    window.localStorage.setItem('user', JSON.stringify({
      uuid: userStore.uuid,
      username: userStore.username,
      email: userStore.email,
      user_type: userStore.userType,
      name: userStore.name,
      avatar: response.data.avatar,
      token: userStore.token
    }))
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    avatarProcessing.value = false
    avatarUpdateDialog.value = false
    avatarCropper.value.destroy()
    avatarCropper.value = null
  }
}

const removeAvatar = async () => {
  avatarProcessing.value = true
  try {
    const response = await axios.delete('/accounts/auth/avatar/')
    userStore.updateAvatar(null)
    window.localStorage.setItem('user', JSON.stringify({
      uuid: userStore.uuid,
      username: userStore.username,
      email: userStore.email,
      user_type: userStore.userType,
      name: userStore.name,
      avatar: null,
      token: userStore.token
    }))
    status.value = response.status
    errors.value = null
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    avatarProcessing.value = false
    avatarRemoveDialog.value = false
  }
}
</script>

<template>
  <v-card
    rounded="lg"
    class="my-5"
  >
    <v-row class="d-flex align-center">
      <v-col
        :cols="12"
        :sm="3"
      >
        <v-img
          :src="userStore.avatar ? userStore.avatar : '/user-avatar.png'"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </v-col>

      <v-col
        :cols="12"
        :sm="9"
      >
        <div class="text-center">
          <small
            v-if="status === 200"
            class="text-success"
          >
            {{ $t('user.avatar_updated_successfully') }}
          </small>
          <small
            v-else-if="status === 204"
            class="text-success"
          >
            {{ $t('user.avatar_removed_successfully') }}
          </small>
          <div
            v-if="errors?.avatar"
            class="text-danger"
          >
            <small v-for="error in errors.avatar">
              {{ error }}
            </small>
          </div>

          <v-card-actions class="d-flex justify-space-evenly">
            <FileInputButton
              @selectedFiles="loadAvatarImg"
              accept="image/*"
              variant="flat"
              color="primary"
              class="text-none"
              :text="$t('user.update_avatar')"
            ></FileInputButton>
            <v-btn
              @click="avatarRemoveDialog = true"
              :disabled="!userStore.avatar"
              variant="outlined"
              class="text-none"
            >
              {{ $t('user.remove_avatar') }}
            </v-btn>
          </v-card-actions>

          <small class="text-secondary">
            {{ $t('form_help.input_img', { width: '500', height: '500' }) }}
          </small>
        </div>
      </v-col>
    </v-row>
  </v-card>

  <v-dialog
    :model-value="avatarUpdateDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <div class="d-flex justify-center align-center">
        <img
          ref="avatarImg"
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
            avatarUpdateDialog = false
            avatarCropper.destroy()
            avatarCropper = null
          }"
          :disabled="avatarImgLoading"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="updateAvatar()"
          :loading="avatarProcessing"
          :disabled="avatarImgLoading"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.update') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="avatarRemoveDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('user.you_want_remove_avatar') }}
      </v-card-title>
      <v-card-text>
        {{ $t('user.avatar_will_be_set_default') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="avatarRemoveDialog = false">
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removeAvatar()"
          :loading="avatarProcessing"
        >
          <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
