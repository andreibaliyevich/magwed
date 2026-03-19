<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import ReportListItemDialog from '../ReportListItemDialog.vue'

const props = defineProps({
  reviewItem: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['reviewUpdated', 'reviewRemoved'])

const reviewProcessing = ref(false)
const reviewRating = ref(0)
const reviewComment = ref('')

const { getLocaleDateTimeString } = useLocaleDateTime()

const reviewMenu = ref(false)
const updateReviewDialog = ref(false)
const removeReviewDialog = ref(false)

const errors = ref(null)

const updateReview = async () => {
  reviewProcessing.value = true
  try {
    const response = await axios.put(
      '/reviews/'
        + props.reviewItem.uuid
        +'/',
      {
        rating: reviewRating.value,
        comment: reviewComment.value
      }
    )
    updateReviewDialog.value = false
    reviewMenu.value = false
    reviewRating.value = 0
    reviewComment.value = ''
    errors.value = null
    emit('reviewUpdated', {
      'rating': response.data.rating,
      'comment': response.data.comment
    })
  } catch (error) {
    errors.value = error.response.data
  } finally {
    reviewProcessing.value = false
  }
}

const removeReview = async () => {
  reviewProcessing.value = true
  try {
    const response = await axios.delete(
      '/reviews/'
        + props.reviewItem.uuid
        +'/'
    )
    if (response.status === 204) {
      removeReviewDialog.value = false
      reviewMenu.value = false
      emit('reviewRemoved')
    }
  } catch (error) {
    console.error(error)
  } finally {
    reviewProcessing.value = false
  }
}
</script>

<template>
  <div class="d-flex ga-3">
    <router-link
      v-if="reviewItem.author.profile_url"
      :to="{
        name: 'OrganizerDetail',
        params: { profile_url: reviewItem.author.profile_url }
      }"
    >
      <AvatarExtended
        :image="reviewItem.author.avatar"
        :size="48"
        :online="reviewItem.author.status === 'online' ? true : false"
      />
    </router-link>
    <AvatarExtended
      v-else
      :image="reviewItem.author.avatar"
      :size="48"
      :online="reviewItem.author.status === 'online' ? true : false"
    />

    <div class="flex-grow-1">
      <div class="d-flex justify-space-between">
        <router-link
          v-if="reviewItem.author.profile_url"
          :to="{
            name: 'OrganizerDetail',
            params: { profile_url: reviewItem.author.profile_url }
          }"
          class="text-decoration-none text-black"
        >
          <strong>{{ reviewItem.author.name }}</strong>
        </router-link>
        <strong v-else>
          {{ reviewItem.author.name }}
        </strong>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(reviewItem.created_at) }}
        </small>
      </div>

      <div class="d-flex justify-space-between">
        <v-rating
          :model-value="reviewItem.rating"
          readonly
          :length="5"
          density="compact"
          size="small"
          color="orange-lighten-1"
        ></v-rating>

        <v-menu
          v-model="reviewMenu"
          location="start"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              icon="mdi-dots-horizontal"
              variant="text"
              size="small"
            ></v-btn>
          </template>
          <v-list density="compact">
            <ReportListItemDialog
              contentType="review"
              :objectUUID="reviewItem.uuid"
              @reportSent="reviewMenu = false"
            />
            <v-list-item
              @click="() => {
                reviewRating = reviewItem.rating
                reviewComment = reviewItem.comment
                updateReviewDialog = true
              }"
              prepend-icon="mdi-pencil"
            >
              {{ $t('btn.edit') }}
            </v-list-item>
            <v-list-item
              @click="removeReviewDialog = true"
              prepend-icon="mdi-delete"
            >
              {{ $t('btn.delete') }}
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
      <div style="white-space: pre-line;">
        {{ reviewItem.comment }}
      </div>
    </div>
  </div>

  <v-dialog
    :model-value="updateReviewDialog"
    :width="500"
    persistent
  >
    <v-card
      :title="$t('reviews.updating_review')"
      rounded="lg"
    >
      <p class="text-subtitle-1 mt-3 mx-3">
        {{ $t('reviews.rating') }}
      </p>
      <v-rating
        v-model="reviewRating"
        :readonly="reviewProcessing"
        :length="5"
        density="default"
        color="orange-lighten-1"
        hover
        class="mx-3"
      ></v-rating>
      <p
        v-if="errors?.rating"
        class="text-error mx-3 mb-3"
      >
        <small
          v-for="error in errors.rating"
          :key="error"
        >
          {{ error }}
        </small>
      </p>

      <v-textarea
        v-model="reviewComment"
        :readonly="reviewProcessing"
        auto-grow
        :rows="5"
        :max-rows="10"
        variant="filled"
        :label="$t('reviews.comment')"
        :error-messages="
          errors?.comment
            ? errors.comment
            : []
        "
        class="mx-3"
      ></v-textarea>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            updateReviewDialog = false
            reviewRating = 0
            reviewComment = ''
            errors = null
          }"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="updateReview()"
          :loading="reviewProcessing"
          :disabled="!reviewRating || !reviewComment"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.update') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="removeReviewDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('reviews.you_want_remove_review') }}
      </v-card-title>
      <v-card-text>
        {{ $t('reviews.organizer_rating_will_be_updated') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="removeReviewDialog = false">
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removeReview()"
          :loading="reviewProcessing"
        >
          <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
