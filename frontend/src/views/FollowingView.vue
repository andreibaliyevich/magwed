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

const followingListLoading = ref(true)
const followingList = ref([])
const followingCount = ref(0)
const nextURL = ref(null)

useHead({
  title: () => t('seo_meta.following.title')
})

const getFollowingList = async () => {
  try {
    const response = await axios.get('/social/follow/list/', {
      params: {
        follower: userStore.uuid
      }
    })
    followingList.value = response.data.results
    followingCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    followingListLoading.value = false
  }
}

const getMoreFollowingList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      followingList.value = [...followingList.value, ...response.data.results]
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
  followingList.value.forEach((element) => {
    if (element.user.uuid === state.user_uuid) {
      element.user.status = state.status
    }
  })
}

onMounted(async () => {
  await getFollowingList()
  connectionBusStore.$subscribe(updateUserStatus)
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('follow.following') }} ({{ followingCount }})
    </h1>

    <div
      v-if="followingListLoading"
      class="d-flex justify-center align-center my-15"
    >
      <v-progress-circular
        indeterminate
        :size="80"
      ></v-progress-circular>
    </div>

    <v-infinite-scroll
      v-else-if="followingList.length > 0"
      @load="getMoreFollowingList"
      mode="intersect"
      empty-text="&nbsp;"
    >
      <v-row class="ma-0">
        <v-col
          v-for="follow in followingList"
          :key="follow.user.uuid"
          :cols="12"
          :sm="6"
          :md="4"
          :lg="3"
          :xl="2"
          class="text-center"
        >
          <router-link
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.user.profile_url }
            }"
            class="d-inline-block"
          >
            <AvatarExtended
              :image="follow.user.avatar"
              :size="180"
              :online="follow.user.status === 'online' ? true : false"
            />
          </router-link>

          <router-link
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: follow.user.profile_url }
            }"
            class="text-black text-decoration-none"
          >
            <h2 class="text-h5">{{ follow.user.name }}</h2>
          </router-link>
        </v-col>
      </v-row>
    </v-infinite-scroll>

    <v-alert
      v-else
      type="info"
      variant="tonal"
      class="my-5"
    >
      {{ $t('follow.no_following') }}
    </v-alert>
  </v-container>
</template>
