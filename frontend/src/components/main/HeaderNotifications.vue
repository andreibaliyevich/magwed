<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { WS_URL } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import HeaderNotice from './HeaderNotice.vue'

const userStore = useUserStore()

const notificationLoading = ref(false)
const notificationList = ref([])
const nextURL = ref(null)
const notViewedCount = ref(0)

const notificationSocket = ref(null)
const notificationSocketConnect = ref(null)

const notificationMenu = ref(false)

const getNotificationList = async () => {
  notificationLoading.value = true
  try {
    const response = await axios.get('/notifications/')
    notificationList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    notificationLoading.value = false
  }
}

const getMoreNotificationList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      notificationList.value = [...notificationList.value, ...response.data.results]
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

const getNotViewedCount = async () => {
  notificationLoading.value = true
  try {
    const response = await axios.get('/notifications/not-viewed-count/')
    notViewedCount.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    notificationLoading.value = false
  }
}

const removeAllNotifications = async () => {
  notificationLoading.value = true
  try {
    const response = await axios.delete('/notifications/list-destroy/')
    if (response.status === 204) {
      notificationList.value = []
      nextURL.value = null
      notViewedCount.value = 0
    }
  } catch (error) {
    console.error(error)
  } finally {
    notificationLoading.value = false
  }
}

const connectSocket = () => {
  notificationSocket.value = new WebSocket(
    WS_URL
      + '/ws/notifications/?'
      + userStore.token
  )
  notificationSocket.value.onopen = (event) => {
    notificationSocketConnect.value = true
  }
  notificationSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action === 'created') {
      notificationList.value.unshift(data.data)
      notViewedCount.value += 1
    } else if (data.action === 'updated') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid === data.data.uuid
      })
      if (foundIndex !== -1) {
        notificationList.value[foundIndex].content_object = data.data.content_object
      }
    } else if (data.action === 'deleted') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid === data.data
      })
      if (foundIndex !== -1) {
        if (!notificationList.value[foundIndex].viewed) {
          notViewedCount.value -= 1
        }
        notificationList.value = notificationList.value.filter((element) => {
          return element.uuid !== data.data
        })
      }
    } else if (data.action === 'viewed') {
      const foundIndex = notificationList.value.findIndex((element) => {
        return element.uuid === data.data.uuid
      })
      if (foundIndex !== -1 && !notificationList.value[foundIndex].viewed) {
        notificationList.value[foundIndex].viewed = data.data.viewed
        notViewedCount.value -= 1
      }
    }
  }
  notificationSocket.value.onclose = (event) => {
    notificationSocket.value = null
    notificationSocketConnect.value = false
  }
  notificationSocket.value.onerror = (error) => {
    notificationSocket.value = null
    notificationSocketConnect.value = false
  }
}

const setNoticeViewed = (isIntersecting, entries, observer) => {
  if (isIntersecting) {
    notificationSocket.value.send(JSON.stringify({
      'notice_uuid': entries[0].target.dataset.uuid
    }))
  }
}

watch(notificationMenu, async (newValue) => {
  if (newValue) {
    await getNotificationList()
  } else {
    notificationList.value = []
    nextURL.value = null
  }
})

onMounted(async () => {
  await getNotViewedCount()
  connectSocket()
})
</script>

<template>
  <v-menu
    v-model="notificationMenu"
    location="bottom end"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        icon
        style="letter-spacing: normal;"
      >
        <v-badge
          v-if="notViewedCount"
          :content="notViewedCount < 10 ? notViewedCount : '9+'"
          color="red-accent-4"
        >
          <v-icon icon="mdi-bell-outline"></v-icon>
        </v-badge>
        <v-icon
          v-else
          icon="mdi-bell-outline"
        ></v-icon>
      </v-btn>
    </template>

    <v-sheet
      :width="350"
      rounded="lg"
      class="px-1 py-1"
    >
      <div class="d-flex justify-space-between align-center px-3 pt-2">
        <div class="text-h6">{{ $t('notifications.notifications') }}</div>
        <v-btn
          @click="removeAllNotifications()"
          :disabled="!notificationList.length"
          density="compact"
          variant="text"
          class="text-none"
        >
          {{ $t('notifications.clear_all') }}
        </v-btn>
      </div>

      <v-divider class="my-1"></v-divider>

      <div
        v-if="notificationLoading"
        class="d-flex justify-center align-center my-15"
      >
        <v-progress-circular
          indeterminate
          :size="50"
        ></v-progress-circular>
      </div>

      <v-infinite-scroll
        v-else-if="notificationList.length > 0"
        @load="getMoreNotificationList"
        mode="intersect"
        :max-height="550"
        :empty-text="$t('notifications.no_more_notifications')"
      >
        <template
          v-for="notice in notificationList"
          :key="notice.uuid"
        >
          <HeaderNotice
            v-if="notice.viewed || !notificationSocketConnect"
            :notice="notice"
          />
          <HeaderNotice
            v-else
            :notice="notice"
            v-intersect="{
              handler: setNoticeViewed,
              options: { threshold: 1.0 }
            }"
          />
          <v-divider class="my-1"></v-divider>
        </template>
      </v-infinite-scroll>

      <div
        v-else
        class="text-center my-5"
      >
        <v-icon
          icon="mdi-clipboard-outline"
          color="secondary"
          :size="100"
        ></v-icon>
        <p class="mt-3">{{ $t('notifications.no_notifications') }}</p>
      </div>
    </v-sheet>
  </v-menu>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 0.2em;
}
</style>
