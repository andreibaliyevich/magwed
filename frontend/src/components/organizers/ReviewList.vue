<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import AuthorReviewItem from './AuthorReviewItem.vue'
import ReviewItem from './ReviewItem.vue'

const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})

const reviewListLoading = ref(true)
const reviewList = ref([])
const nextURL = ref(null)

const reviewSending = ref(false)
const reviewRating = ref(0)
const reviewComment = ref('')

const errors = ref(null)

const getReviewList = async () => {
  try {
    const response = await axios.get('/reviews/', {
      params: {
        user: props.userUUID
      }
    })
    reviewList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    reviewListLoading.value = false
  }
}

const getMoreReviewList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      reviewList.value = [...reviewList.value, ...response.data.results]
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

const sendReview = async () => {
  reviewSending.value = true
  try {
    const response = await axios.post('/reviews/', {
      user: props.userUUID,
      rating: reviewRating.value,
      comment: reviewComment.value
    })
    reviewList.value.unshift(response.data)
    reviewRating.value = 0
    reviewComment.value = ''
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  } finally {
    reviewSending.value = false
  }
}

const updateReview = (reviewIndex, data) => {
  reviewList.value[reviewIndex].rating = data.rating
  reviewList.value[reviewIndex].comment = data.comment
}

const removeReview = (reviewUuid) => {
  reviewList.value = reviewList.value.filter((element) => {
    return element.uuid !== reviewUuid
  })
}

const updateUserStatus = (mutation, state) => {
  reviewList.value.forEach((element) => {
    if (element.author.uuid === state.user_uuid) {
      element.author.status = state.status
    }
  })
}

onMounted(async () => {
  await getReviewList()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <v-row class="flex-md-row-reverse">
    <v-col
      :cols="12"
      :md="6"
    >
      <v-card
        v-if="userStore.isLoggedIn"
        :title="$t('reviews.write_review')"
        rounded="lg"
      >
        <p class="text-subtitle-1 mx-3">
          {{ $t('reviews.rating') }}
        </p>
        <v-rating
          v-model="reviewRating"
          :readonly="reviewSending"
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
          :readonly="reviewSending"
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

        <p
          v-if="errors?.create"
          class="text-error mx-3"
        >
          {{ errors.create }}
        </p>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            @click="sendReview()"
            :loading="reviewSending"
            :disabled="!reviewRating || !reviewComment"
            variant="flat"
            color="primary"
          >
            {{ $t('btn.send') }}
          </v-btn>
        </v-card-actions>
      </v-card>

      <v-alert
        v-else
        type="info"
        variant="tonal"
      >
        {{ $t('reviews.need_log_in') }}
        <router-link
          :to="{
            name: 'Login',
            query: { redirect: $route.path }
          }"
          class="font-weight-bold"
        >
          {{ $t('auth.log_in') }}
        </router-link>
      </v-alert>
    </v-col>

    <v-col
      :cols="12"
      :md="6"
    >
      <div
        v-if="reviewListLoading"
        class="d-flex justify-center align-center my-15"
      >
        <v-progress-circular
          indeterminate
          :size="80"
        ></v-progress-circular>
      </div>

      <v-infinite-scroll
        v-else-if="reviewList.length > 0"
        @load="getMoreReviewList"
        mode="intersect"
        empty-text="&nbsp;"
      >
        <TransitionGroup
          tag="ul"
          name="list-group"
        >
          <li
            v-for="(reviewItem, reviewIndex) in reviewList"
            :key="reviewItem.uuid"
            class="d-block my-5"
          >
            <AuthorReviewItem
              v-if="reviewItem.author.uuid === userStore.uuid"
              :reviewItem="reviewItem"
              @reviewUpdated="(data) => {
                updateReview(reviewIndex, data)
              }"
              @reviewRemoved="removeReview(reviewItem.uuid)"
            />
            <ReviewItem
              v-else
              :reviewItem="reviewItem"
            />
          </li>
        </TransitionGroup>
      </v-infinite-scroll>

      <p
        v-else
        class="text-body-1 mx-1 my-5"
      >
        {{ $t('reviews.no_reviews_yet') }}
      </p>
    </v-col>
  </v-row>
</template>

<style scoped>
.list-group-move,
.list-group-enter-active,
.list-group-leave-active {
  transition: all 0.5s ease;
}
.list-group-enter-from,
.list-group-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
.list-group-leave-active {
  position: absolute;
}
</style>
