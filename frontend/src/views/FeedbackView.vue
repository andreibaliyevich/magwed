<script setup>
import axios from 'axios'
import { useSeoMeta } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

const { t, locale } = useI18n({ useScope: 'global' })

const loadingStatus = ref(false)

const subject = ref(null)
const email = ref('')
const comment = ref('')

const subjectOptions = ref([])

const status = ref(null)
const errors = ref(null)

useSeoMeta({
  title: () => t('seo_meta.feedback.title'),
  ogTitle: () => t('seo_meta.feedback.title'),
  description: () => t('seo_meta.feedback.description'),
  ogDescription: () => t('seo_meta.feedback.description'),
  keywords: () => t('seo_meta.feedback.keywords'),
  ogKeywords: () => t('seo_meta.feedback.keywords')
})

const setSubjectOptions = () => {
  subjectOptions.value = [
    { value: 1, title: t('feedback.subject_options.1') },
    { value: 2, title: t('feedback.subject_options.2') },
    { value: 3, title: t('feedback.subject_options.3') },
    { value: 4, title: t('feedback.subject_options.4') },
    { value: 5, title: t('feedback.subject_options.5') }
  ]
}

const sendFeedback = async () => {
  loadingStatus.value = true

  try {
    const response = await axios.post('/support/feedback/', {
      subject: subject.value,
      email: email.value,
      comment: comment.value
    })
    if (response.status === 201) {
      subject.value = null
      email.value = ''
      comment.value = ''
      status.value = 201
      errors.value = null
    }
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
  }
}

watch(locale, () => {
  setSubjectOptions()
})

onMounted(() => {
  setSubjectOptions()
})
</script>

<template>
  <v-container class="my-5">
    <h1 class="text-h3 text-center mb-5">
      {{ $t('feedback.feedback') }}
    </h1>

    <v-row
      align="center"
      justify="center"
    >
      <v-col
        xs="12"
        sm="10"
        md="8"
        lg="6"
        xl="5"
        xxl="4"
      >
        <p class="text-subtitle-1 mb-5">
          {{ $t('feedback.message1') }}
        </p>

        <v-alert
          v-if="status === 201"
          type="success"
          variant="tonal"
          closable
        >
          {{ $t('feedback.status201') }}
        </v-alert>

        <v-form
          @submit.prevent="sendFeedback()"
          class="mt-5"
        >
          <v-select
            v-model="subject"
            :items="subjectOptions"
            item-title="title"
            item-value="value"
            :readonly="loadingStatus"
            variant="filled"
            :label="$t('feedback.subject')"
            :error-messages="errors?.subject ? errors.subject : []"
          ></v-select>
          <v-text-field
            v-model="email"
            :readonly="loadingStatus"
            variant="filled"
            type="email"
            :label="$t('feedback.email')"
            :error-messages="errors?.email ? errors.email : []"
          ></v-text-field>
          <v-textarea
            v-model="comment"
            :label="$t('feedback.comment')"
            :error-messages="errors?.comment ? errors.comment : []"
          ></v-textarea>
          <v-btn
            :loading="loadingStatus"
            type="submit"
            variant="flat"
            color="primary"
            size="x-large"
            block
            class="mt-2"
          >
            {{ $t('btn.send') }}
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>
