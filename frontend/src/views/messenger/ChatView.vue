<script setup>
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { WS_URL, chatType, messageType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import AuthorMessageItem from '@/components/messenger/AuthorMessageItem.vue'
import MessageItem from '@/components/messenger/MessageItem.vue'
import ReportListItemDialog from '@/components/ReportListItemDialog.vue'

const emit = defineEmits(['msgViewed', 'leaveChat'])

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const chatDataLoading = ref(false)
const chatDataProcessing = ref(false)
const chatData = ref({
  uuid: '',
  chat_type: null,
  details: {
    uuid: '',
    name: '',
    avatar: '',
    status: null,
    profile_url: null
  }
})

const groupChatDataLoading = ref(false)
const groupChatData = ref({
  uuid: '',
  members: [],
  group_details: {
    owner: '',
    name: '',
    image: null
  }
})

const messageListLoading = ref(false)
const messageList = ref([])
const nextURL = ref(null)

const chatSocket = ref(null)
const chatSocketConnect = ref(false)

const messageSending = ref(false)
const textContent = ref('')

const { getLocaleDateTimeString } = useLocaleDateTime()

const errors = ref(null)
const errorStatus = ref(null)

const messageListArea = ref(null)
const msgTextarea = ref(null)

const chatMenu = ref(false)
const groupDetailDialog = ref(false)
const removeChatDialog = ref(false)
const leaveChatDialog = ref(false)

const reversedMessages = computed(() => {
  return [...messageList.value].reverse()
})

const getMessageList = async () => {
  messageListLoading.value = true
  try {
    const response = await axios.get('/messenger/message/list/', {
      params: {
        chat: chatData.value.uuid
      }
    })
    messageList.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    messageListLoading.value = false
    msgTextarea.value.focus()
  }
}

const getMoreMessageList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      messageList.value = [...messageList.value, ...response.data.results]
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

const openChatSocket = () => {
  chatSocket.value = new WebSocket(
    WS_URL
      + '/ws/chat/'
      + chatData.value.uuid
      + '/?'
      + userStore.token
  )
  chatSocket.value.onopen = (event) => {
    chatSocketConnect.value = true
  }
  chatSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action === 'new_msg') {
      messageList.value.unshift(data.data)
      nextTick(() => {
        messageListArea.value.$el.scrollTo({
          top: messageListArea.value.$el.scrollHeight,
          behavior: 'smooth'
        })
      })
    } else if (data.action === 'viewed') {
      const foundIndex = messageList.value.findIndex((element) => {
        return element.uuid === data.data.msg_uuid
      })
      if (foundIndex !== -1) {
        messageList.value[foundIndex].viewed_by.push(data.data.msg_viewed_by)
      }
    }
  }
  chatSocket.value.onclose = (event) => {
    chatSocket.value = null
    chatSocketConnect.value = false
  }
  chatSocket.value.onerror = (error) => {
    chatSocket.value = null
    chatSocketConnect.value = false
  }
}

const closeChatSocket = () => {
  if (chatSocket.value) {
    chatSocket.value.close()
  }
}

const getChatData = async () => {
  chatDataLoading.value = true
  try {
    const response = await axios.get(
      '/messenger/chat/retrieve/'
        + route.params.uuid
        +'/'
    )
    chatData.value = response.data
    getMessageList()
    openChatSocket()
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    chatDataLoading.value = false
  }
}

const getGroupChatData = async () => {
  groupChatDataLoading.value = true
  try {
    const response = await axios.get(
      '/messenger/chat/group-retrieve/'
        + chatData.value.uuid
        +'/'
    )
    groupChatData.value = response.data
  } catch (error) {
    errorStatus.value = error.response.status
  } finally {
    groupChatDataLoading.value = false
  }
}

const sendTextMessage = async () => {
  messageSending.value = true
  try {
    const response = await axios.post(
      '/messenger/message/new/'
        + chatData.value.uuid
        + '/'
        + messageType.TEXT
        + '/',
      { content: textContent.value }
    )
    if (response.status === 201) {
      textContent.value = ''
      msgTextarea.value.focus()
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

const sendImageMessage = async (filelist) => {
  messageSending.value = true

  let formData = new FormData()
  for (let i = 0; i < filelist.length; i++) {
    formData.append('content', filelist[i], filelist[i].name)
  }

  try {
    const response = await axios.post(
      '/messenger/message/new/'
        + chatData.value.uuid
        + '/'
        + messageType.IMAGES
        + '/',
      formData
    )
    if (response.status === 201) {
      msgTextarea.value.focus()
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

const sendFileMessage = async (filelist) => {
  messageSending.value = true

  let formData = new FormData()
  for (let i = 0; i < filelist.length; i++) {
    formData.append('content', filelist[i], filelist[i].name)
  }

  try {
    const response = await axios.post(
      '/messenger/message/new/'
        + chatData.value.uuid
        + '/'
        + messageType.FILES
        + '/',
      formData
    )
    if (response.status === 201) {
      msgTextarea.value.focus()
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    messageSending.value = false
  }
}

const setMessageViewed = (isIntersecting, entries, observer) => {
  if (isIntersecting) {
    chatSocket.value.send(JSON.stringify({
      action: 'viewed',
      msg_uuid: entries[0].target.dataset.uuid
    }))
    emit('msgViewed')
  }
}

const removeChat = async () => {
  chatDataProcessing.value = true
  try {
    const response = await axios.delete(
      '/messenger/chat/destroy/'
        + chatData.value.uuid
        +'/'
    )
    if (response.status === 204) {
      removeChatDialog.value = false
      chatMenu.value = false
    }
  } catch (error) {
    console.error(error)
  } finally {
    chatDataProcessing.value = false
  }
}

const leaveChat = async () => {
  try {
    const response = await axios.delete(
      '/messenger/chat/leave/'
        + chatData.value.uuid
        +'/'
    )
    if (response.status === 204) {
      leaveChatDialog.value = false
      chatMenu.value = false
      emit('leaveChat', chatData.value.uuid)
      router.push({ name: 'Messenger' })
    }
  } catch (error) {
    console.error(error)
  }
}

const updateUserStatus = (mutation, state) => {
  if (chatData.value.details.uuid === state.user_uuid) {
    chatData.value.details.status = state.status
  }
  messageList.value.forEach((element) => {
    if (element.author.uuid === state.user_uuid) {
      element.author.status = state.status
    }
  })
}

watch(
  () => route.params.uuid,
  async () => {
    if (route.name === 'Chat') {
      messageList.value = []
      nextURL.value = null
      errorStatus.value = null
      closeChatSocket()
      await getChatData()
    }
  }
)

onMounted(async () => {
  await getChatData()
  connectionBusStore.$subscribe(updateUserStatus)
})

onUnmounted(() => {
  closeChatSocket()
})
</script>

<template>
  <div
    v-if="chatDataLoading"
    class="d-flex justify-center align-center my-10"
  >
    <v-progress-circular
      indeterminate
      :size="50"
    ></v-progress-circular>
  </div>

  <v-sheet
    v-else-if="errorStatus === 404"
    height="100%"
    min-height="75vh"
    class="d-flex justify-center align-center"
  >
    <div class="text-center">
      <v-icon
        icon="mdi-chat-question-outline"
        :size="150"
        color="secondary"
      ></v-icon>
      <p class="text-h5 mt-3">{{ $t('errors.chat_not_found') }}</p>
    </div>
  </v-sheet>

  <div v-else>
    <div
      v-if="chatData.chat_type === chatType.DIALOG"
      class="d-flex align-center ga-3 border-b-sm"
    >
      <v-avatar
        :image="
          chatData.details.avatar
            ? chatData.details.avatar
            : '/user-avatar.png'
        "
        :size="48"
      ></v-avatar>
      <div class="d-inline-block">
        <h6 class="text-h6">{{ chatData.details.name }}</h6>
        <span
          v-if="chatData.details.status === 'online'"
          class="d-flex align-center text-black"
        >
          <v-icon
            icon="mdi-circle"
            :size="16"
            color="green-darken-3"
            class="me-1"
          ></v-icon>
          {{ $t('user.online') }}
        </span>
        <span
          v-else
          class="d-flex align-center text-secondary"
        >
          <v-icon
            icon="mdi-circle"
            :size="16"
            class="me-1"
          ></v-icon>
          {{ $t('user.last_visit') }}
          {{ getLocaleDateTimeString(chatData.details.status) }}
        </span>
      </div>
      <v-menu
        v-model="chatMenu"
        location="start"
        :close-on-content-click="false"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            icon="mdi-dots-vertical"
            variant="text"
            class="ms-auto"
          ></v-btn>
        </template>
        <v-list density="compact">
          <v-list-item
            v-if="chatData.details.profile_url"
            :to="{
              name: 'OrganizerDetail',
              params: { profile_url: chatData.details.profile_url }
            }"
            prepend-icon="mdi-account"
          >
            {{ $t('user.view_profile') }}
          </v-list-item>
          <ReportListItemDialog
            contentType="user"
            :objectUUID="chatData.details.uuid"
            @reportSent="chatMenu = false"
          />
          <v-list-item
            @click="removeChatDialog = true"
            prepend-icon="mdi-delete"
          >
            {{ $t('messenger.delete_chat') }}
          </v-list-item>
        </v-list>
      </v-menu>
    </div>

    <div
      v-else-if="chatData.chat_type === chatType.GROUP"
      class="d-flex align-center ga-3 border-b-sm"
    >
      <v-avatar
        :image="
          chatData.details.image
            ? chatData.details.image
            : '/group-avatar.jpg'
        "
        :size="48"
      ></v-avatar>
      <div class="d-inline-block">
        <h6 class="text-h6">{{ chatData.details.name }}</h6>
        <span class="text-secondary">
          {{ $t('messenger.member_count', {n: chatData.details.member_count}) }}
        </span>
      </div>
      <v-menu
        v-model="chatMenu"
        location="start"
        :close-on-content-click="false"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            icon="mdi-dots-vertical"
            variant="text"
            class="ms-auto"
          ></v-btn>
        </template>
        <v-list density="compact">
          <v-list-item
            @click="() => {
              getGroupChatData()
              groupDetailDialog = true
            }"
            prepend-icon="mdi-account-group"
          >
            {{ $t('messenger.view_group_detail') }}
          </v-list-item>
          <v-list-item
            v-if="chatData.details.owner === userStore.uuid"
            @click="removeChatDialog = true"
            prepend-icon="mdi-delete"
          >
            {{ $t('messenger.delete_chat') }}
          </v-list-item>
          <v-list-item
            v-else
            @click="leaveChatDialog = true"
            prepend-icon="mdi-delete"
          >
            {{ $t('messenger.leave_group') }}
          </v-list-item>
        </v-list>
      </v-menu>
    </div>

    <div
      v-else
      class="d-flex align-center ga-3 border-b-sm"
    >
      <v-avatar
        image="/chat.jpg"
        :size="48"
      ></v-avatar>
    </div>

    <v-sheet height="65vh">
      <div
        v-if="messageListLoading"
        class="d-flex justify-center align-center h-100"
      >
        <v-progress-circular
          indeterminate
          :size="50"
        ></v-progress-circular>
      </div>

      <v-infinite-scroll
        v-else-if="messageList.length > 0"
        ref="messageListArea"
        @load="getMoreMessageList"
        mode="intersect"
        side="start"
        height="100%"
        empty-text="&nbsp;"
      >
        <div
          v-for="msg in reversedMessages"
          class="my-1 mx-1"
        >
          <AuthorMessageItem
            v-if="msg.author.uuid === userStore.uuid"
            :msg="msg"
          />
          <MessageItem
            v-else-if="msg.viewed_by.includes(userStore.uuid) || !chatSocketConnect"
            :chatTypeData="chatData.chat_type"
            :msg="msg"
          />
          <MessageItem
            v-else
            :chatTypeData="chatData.chat_type"
            :msg="msg"
            v-intersect="{
              handler: setMessageViewed,
              options: { threshold: 1.0 }
            }"
          />
        </div>
      </v-infinite-scroll>

      <div
        v-else
        class="d-flex flex-column justify-center align-center h-100"
      >
        <v-icon
          icon="mdi-message-outline"
          :size="150"
          color="secondary"
        ></v-icon>
        <p class="text-h5 mt-3">{{ $t('messenger.no_messages') }}</p>
      </div>
    </v-sheet>

    <v-progress-linear
      v-if="messageSending"
      indeterminate
    ></v-progress-linear>
    <div class="d-flex justify-center align-center ga-1 border-t-sm pt-1">
      <FileInputButton
        @selectedFiles="sendImageMessage"
        accept="image/*"
        multiple
        variant="text"
        icon="mdi-file-image-outline"
      ></FileInputButton>
      <FileInputButton
        @selectedFiles="sendFileMessage"
        multiple
        variant="text"
        icon="mdi-file-outline"
      ></FileInputButton>
      <v-textarea
        ref="msgTextarea"
        v-model="textContent"
        :readonly="messageSending"
        auto-grow
        :rows="1"
        :max-rows="10"
        variant="solo-filled"
        flat
        :placeholder="$t('messenger.type_message')"
        :append-inner-icon="textContent ? 'mdi-send' : ''"
        @click:append-inner="sendTextMessage()"
        @keyup.ctrl.enter="sendTextMessage()"
        :hide-details="!errors?.content"
        :error-messages="errors?.content ? errors.content : []"
      ></v-textarea>
    </div>
  </div>

  <v-dialog
    v-model="groupDetailDialog"
    :width="500"
  >
    <v-card
      rounded="lg"
      :title="$t('messenger.group_chat_details')"
    >
      <div
        v-if="groupChatDataLoading"
        class="d-flex justify-center align-center my-10"
      >
        <v-progress-circular
          indeterminate
          :size="50"
        ></v-progress-circular>
      </div>

      <div
        v-else
        class="mt-3 mx-3"
      >
        <div class="d-flex align-center ga-3">
          <v-avatar
            :image="
              groupChatData.group_details.image
                ? groupChatData.group_details.image
                : '/group-avatar.jpg'
            "
            :size="64"
          ></v-avatar>
          <div class="d-inline-block">
            <h6 class="text-h6">{{ groupChatData.group_details.name }}</h6>
            <span class="text-secondary">
              {{ $t('messenger.member_count', {n: groupChatData.members.length}) }}
            </span>
          </div>
        </div>

        <p class="text-subtitle-1 mt-3">{{ $t('messenger.members') }}:</p>
        <v-list v-if="groupChatData.members.length > 0">
          <v-list-item
            v-for="user in groupChatData.members"
            :key="user.uuid"
          >
            <template v-slot:prepend>
              <router-link
                v-if="user.profile_url"
                :to="{
                  name: 'OrganizerDetail',
                  params: { profile_url: user.profile_url }
                }"
                class="me-3"
              >
                <v-avatar
                  :image="user.avatar ? user.avatar : '/user-avatar.png'"
                  :size="48"
                ></v-avatar>
              </router-link>
              <div
                v-else
                class="me-3"
              >
                <v-avatar
                  :image="user.avatar ? user.avatar : '/user-avatar.png'"
                  :size="48"
                ></v-avatar>
              </div>
            </template>

            <v-list-item-title>
              <router-link
                v-if="user.profile_url"
                :to="{
                  name: 'OrganizerDetail',
                  params: { profile_url: user.profile_url }
                }"
                class="text-decoration-none text-black"
              >
                <span class="text-subtitle-1 font-weight-medium">
                  {{ user.name }}
                </span>
              </router-link>
              <span
                v-else
                class="text-subtitle-1 font-weight-medium"
              >
                {{ user.name }}
              </span>
            </v-list-item-title>
            <v-list-item-subtitle>
              <span
                v-if="user.status === 'online'"
                class="d-flex align-center"
              >
                <v-icon
                  icon="mdi-circle"
                  :size="16"
                  color="green-darken-3"
                  class="me-1"
                ></v-icon>
                {{ $t('user.online') }}
              </span>
              <span
                v-else
                class="d-flex align-center"
              >
                <v-icon
                  icon="mdi-circle"
                  :size="16"
                  class="me-1"
                ></v-icon>
                {{ $t('user.last_visit') }}
                {{ getLocaleDateTimeString(user.status) }}
              </span>
            </v-list-item-subtitle>

            <template
              v-if="user.uuid === groupChatData.group_details.owner"
              v-slot:append
            >
              <v-icon
                icon="mdi-star"
                color="orange-darken-1"
              ></v-icon>
            </template>
          </v-list-item>
        </v-list>

        <v-alert
          v-else
          type="info"
          variant="tonal"
          class="my-1"
        >
          {{ $t('messenger.member_list_empty') }}
        </v-alert>
      </div>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="groupDetailDialog = false">
          {{ $t('btn.close') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="removeChatDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('messenger.you_want_remove_chat') }}
      </v-card-title>
      <v-card-text>
        {{ $t('messenger.chat_messages_will_lost') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="removeChatDialog = false">
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removeChat()"
          :loading="chatDataProcessing"
        >
          <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="leaveChatDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('messenger.you_want_leave_chat') }}
      </v-card-title>
      <v-card-text>
        {{ $t('messenger.you_will_lose_access_chat_messages') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="leaveChatDialog = false">
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="leaveChat()"
          :loading="chatDataProcessing"
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
