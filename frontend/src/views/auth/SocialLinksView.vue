<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

const { t, locale } = useI18n({ useScope: 'global' })

const socialLinkListLoading = ref(true)
const socialLinkListUpdating = ref(false)
const socialLinkList = ref([])

const socialLinkUuid = ref(null)
const socialLinkType = ref(null)
const socialLinkUrl = ref('')

const linkTypeOptions = ref([])

const socialLinkAddDialog = ref(null)
const socialLinkUpdateDialog = ref(null)

const errors = ref(null)

useHead({
  title: () => t('seo_meta.social_links.title')
})

const setLinkTypeOptions = () => {
  linkTypeOptions.value = [
    { value: 'facebook', title: t('auth.sociallinks.facebook') },
    { value: 'twitter', title: t('auth.sociallinks.twitter') },
    { value: 'instagram', title: t('auth.sociallinks.instagram') },
    { value: 'linkedin', title: t('auth.sociallinks.linkedin') },
    { value: 'spotify', title: t('auth.sociallinks.spotify') },
    { value: 'youtube', title: t('auth.sociallinks.youtube') },
    { value: 'soundcloud', title: t('auth.sociallinks.soundcloud') },
    { value: 'pinterest', title: t('auth.sociallinks.pinterest') }
  ]
}

const getSocialLinks = async () => {
  try {
    const response = await axios.get('/social/links/')
    socialLinkList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    socialLinkListLoading.value = false
  }
}

const addSocialLink = async () => {
  socialLinkListUpdating.value = true
  try {
    const response = await axios.post('/social/links/', {
      link_type: socialLinkType.value,
      link_url: socialLinkUrl.value
    })
    socialLinkList.value.push(response.data)
    socialLinkAddDialog.value = false
    socialLinkType.value = null
    socialLinkUrl.value = ''
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  } finally {
    socialLinkListUpdating.value = false
  }
}

const updateSocialLink = async () => {
  socialLinkListUpdating.value = true
  try {
    const response = await axios.put(
      '/social/links/'
        + socialLinkUuid.value
        +'/',
      {
        link_type: socialLinkType.value,
        link_url: socialLinkUrl.value
      }
    )
    const foundIndex = socialLinkList.value.findIndex((element) => {
      return element.uuid === socialLinkUuid.value
    })
    socialLinkList.value[foundIndex] = response.data
    socialLinkUpdateDialog.value = false
    socialLinkUuid.value = null
    socialLinkType.value = null
    socialLinkUrl.value = ''
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  } finally {
    socialLinkListUpdating.value = false
  }
}

const removeSocialLink = async (slUuid) => {
  try {
    const response = await axios.delete('/social/links/' + slUuid +'/')
    if (response.status === 204) {
      socialLinkList.value = socialLinkList.value.filter((element) => {
        return element.uuid !== slUuid
      })
    }
  } catch (error) {
    console.error(error)
  }
}

watch(locale, () => {
  setLinkTypeOptions()
})

onMounted(async () => {
  setLinkTypeOptions()
  await getSocialLinks()
})
</script>

<template>
  <h1 class="text-h4 text-md-h3 text-center my-5">
    {{ $t('auth.sociallinks.social_links') }}
  </h1>

  <div
    v-if="socialLinkListLoading"
    class="d-flex justify-center align-center my-15"
  >
    <v-progress-circular
      indeterminate
      :size="80"
    ></v-progress-circular>
  </div>

  <v-list v-else-if="socialLinkList.length > 0">
    <v-list-item
      v-for="socialLinkItem in socialLinkList"
      :key="socialLinkItem.uuid"
      :prepend-icon="`mdi-${socialLinkItem.link_type}`"
    >
      <a
        :href="socialLinkItem.link_url"
        target="_blank"
        class="text-indigo"
      >
        {{ socialLinkItem.link_url }}
      </a>
      <template v-slot:append>
        <v-btn
          @click="() => {
            socialLinkUuid = socialLinkItem.uuid
            socialLinkType = socialLinkItem.link_type
            socialLinkUrl = socialLinkItem.link_url
            socialLinkUpdateDialog = true
          }"
          variant="text"
          color="grey-darken-3"
          icon="mdi-pencil"
        ></v-btn>
        <v-btn
          @click="removeSocialLink(socialLinkItem.uuid)"
          variant="text"
          color="red-darken-3"
          icon="mdi-delete"
        ></v-btn>
      </template>
    </v-list-item>
  </v-list>

  <v-alert
    v-else
    type="info"
    variant="tonal"
  >
    {{ $t('auth.sociallinks.do_not_have_social_links') }}
  </v-alert>

  <v-btn
    @click="socialLinkAddDialog = true"
    variant="flat"
    color="primary"
    size="large"
    class="text-none mt-3 mb-10"
    append-icon="mdi-plus-circle-outline"
  >
    {{ $t('auth.sociallinks.add_link') }}
  </v-btn>

  <v-dialog
    :model-value="socialLinkAddDialog"
    :width="500"
    persistent
  >
    <v-card
      :title="$t('auth.sociallinks.adding_a_link')"
      rounded="lg"
    >
      <v-row
        dense
        class="pa-5"
      >
        <v-col
          :cols="12"
          :md="12"
        >
          <v-select
            v-model="socialLinkType"
            :items="linkTypeOptions"
            item-title="title"
            item-value="value"
            :readonly="socialLinkListUpdating"
            variant="filled"
            :label="$t('auth.sociallinks.type_of_link')"
            :error-messages="errors?.link_type ? errors.link_type : []"
          ></v-select>
        </v-col>
        <v-col
          :cols="12"
          :md="12"
        >
          <v-text-field
            v-model="socialLinkUrl"
            :readonly="socialLinkListUpdating"
            type="url"
            maxlength="200"
            variant="filled"
            :label="$t('auth.sociallinks.url_of_link')"
            :error-messages="errors?.link_url ? errors.link_url : []"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            socialLinkAddDialog = false
            socialLinkType = null
            socialLinkUrl = ''
            errors = null
          }"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="addSocialLink()"
          :loading="socialLinkListUpdating"
          :disabled="!socialLinkType || !socialLinkUrl"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.add') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="socialLinkUpdateDialog"
    :width="500"
    persistent
  >
    <v-card
      :title="$t('auth.sociallinks.changing_the_link')"
      rounded="lg"
    >
      <v-row
        dense
        class="pa-5"
      >
        <v-col
          :cols="12"
          :md="12"
        >
          <v-select
            v-model="socialLinkType"
            :items="linkTypeOptions"
            item-title="title"
            item-value="value"
            :readonly="socialLinkListUpdating"
            variant="filled"
            :label="$t('auth.sociallinks.type_of_link')"
            :error-messages="errors?.link_type ? errors.link_type : []"
          ></v-select>
        </v-col>
        <v-col
          :cols="12"
          :md="12"
        >
          <v-text-field
            v-model="socialLinkUrl"
            :readonly="socialLinkListUpdating"
            type="url"
            maxlength="200"
            variant="filled"
            :label="$t('auth.sociallinks.url_of_link')"
            :error-messages="errors?.link_url ? errors.link_url : []"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            socialLinkUpdateDialog = false
            socialLinkUuid = null
            socialLinkType = null
            socialLinkUrl = ''
            errors = null
          }"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="updateSocialLink()"
          :loading="socialLinkListUpdating"
          :disabled="!socialLinkType || !socialLinkUrl"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.update') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
