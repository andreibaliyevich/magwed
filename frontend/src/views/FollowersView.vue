<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'

const { t } = useI18n({ useScope: 'global' })
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const followersListLoading = ref(true)
const followersList = ref([])
const followersCount = ref(0)
const nextURL = ref(null)

useHead({
  title: () => t('seo_meta.followers.title')
})

const getFollowersList = async () => {
  try {
    const response = await axios.get('/social/follow/list/', {
      params: {
        user: userStore.uuid
      }
    })
    followersList.value = response.data.results
    followersCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followersListLoading.value = false
  }
}

const getMoreFollowersList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      followersList.value = [...followersList.value, ...response.data.results]
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

const updateUserStatus = (mutation, state) => {
  followersList.value.forEach((element) => {
    if (element.follower.uuid === state.user_uuid) {
      element.follower.status = state.status
    }
  })
}

onMounted(async () => {
  await getFollowersList()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('follow.followers') }} ({{ followersCount }})
    </h1>

    <div
      v-if="followersListLoading"
      class="d-flex justify-center align-center my-15"
    >
      <v-progress-circular
        indeterminate
        :size="80"
      ></v-progress-circular>
    </div>

    <v-infinite-scroll
      v-else-if="followersList.length > 0"
      @load="getMoreFollowersList"
      mode="intersect"
      empty-text="&nbsp;"
    >
      <v-row class="ma-0">
        <v-col
          v-for="follow in followersList"
          :key="follow.follower.uuid"
          :cols="12"
          :sm="6"
          :md="4"
          :lg="3"
          :xl="2"
          class="text-center"
        >
          <router-link
            v-if="follow.follower.profile_url"
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.follower.profile_url }
            }"
            class="d-inline-block"
          >
            <AvatarExtended
              :image="follow.follower.avatar"
              :size="180"
              :online="follow.follower.status === 'online' ? true : false"
            />
          </router-link>
          <div
            v-else
            class="d-inline-block"
          >
            <AvatarExtended
              :image="follow.follower.avatar"
              :size="180"
              :online="follow.follower.status === 'online' ? true : false"
            />
          </div>

          <router-link
            v-if="follow.follower.profile_url"
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.follower.profile_url }
            }"
            class="text-black text-decoration-none"
          >
            <h2 class="text-h5">{{ follow.follower.name }}</h2>
          </router-link>
          <h2
            v-else
            class="text-h5"
          >
            {{ follow.follower.name }}
          </h2>
        </v-col>
      </v-row>
    </v-infinite-scroll>

    <v-alert
      v-else
      type="info"
      variant="tonal"
      class="my-5"
    >
      {{ $t('follow.no_followers') }}
    </v-alert>
  </v-container>
</template>
