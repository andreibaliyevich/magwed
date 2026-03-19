<script setup>
import axios from 'axios'
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { WS_URL, chatType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import ChatList from '@/components/messenger/ChatList.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n({ useScope: 'global' })
const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const chatListLoading = ref(true)
const chatList = ref([])
const nextURL = ref(null)

const chatListSocket = ref(null)

const relatedUserListLoading = ref(false)
const relatedUserList = ref([])
const relatedUserListNextURL = ref(null)

const chatCreating = ref(false)
const selectedChatType = ref(chatType.DIALOG)
const selectedMembers = ref([])
const groupChatName = ref('')
const groupChatImage = ref(null)

const errors = ref(null)

const chatListDrawer = ref(false)
const createChatDialog = ref(false)

const chatIndex = computed(() => {
  return chatList.value.findIndex((element) => {
    return element.uuid === route.params.uuid
  })
})

const chatCreationDisabled = computed(() => {
  if (
    selectedChatType.value === chatType.DIALOG &&
    selectedMembers.value.length > 0
  ) {
    return false
  }
  if (
    selectedChatType.value === chatType.GROUP &&
    selectedMembers.value.length > 0 &&
    groupChatName.value
  ) {
    return false
  }
  return true
})

useHead({
  title: () => t('seo_meta.messenger.title')
})

const openChatListSocket = () => {
  chatListSocket.value = new WebSocket(
    WS_URL
      + '/ws/chat-list/?'
      + userStore.token
  )
  chatListSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action === 'create_chat') {
      chatList.value.push(data.data)
    } else if (data.action === 'destroy_chat') {
      chatList.value = chatList.value.filter((element) => {
        return element.uuid !== data.data
      })
      if (data.data === route.params.uuid) {
        router.push({ name: 'Messenger' })
      }
    } else if (data.action === 'new_msg') {
      const foundIndex = chatList.value.findIndex((element) => {
        return element.uuid === data.data.chat_uuid
      })
      chatList.value[foundIndex].last_message = data.data.msg
      if (data.data.author_uuid !== userStore.uuid) {
        chatList.value[foundIndex].unviewed_msg_count += 1
      }
    }
  }
  chatListSocket.value.onclose = (event) => {
    chatListSocket.value = null
  }
  chatListSocket.value.onerror = (error) => {
    chatListSocket.value = null
  }
}

const closeChatListSocket = () => {
  if (chatListSocket.value) {
    chatListSocket.value.close()
  }
}

const getChatList = async () => {
  try {
    const response = await axios.get('/messenger/chat/list/')
    chatList.value = response.data.results
    nextURL.value = response.data.next
    openChatListSocket()
  } catch (error) {
    console.error(error)
  } finally {
    chatListLoading.value = false
  }
}

const getMoreChatList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      chatList.value = [...chatList.value, ...response.data.results]
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

const getRelatedUserList = async () => {
  relatedUserListLoading.value = true
  try {
    const response = await axios.get('/social/follow/related-users/')
    relatedUserList.value = response.data.results
    relatedUserListNextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    relatedUserListLoading.value = false
  }
}

const getMoreRelatedUserList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(relatedUserListNextURL.value)
      relatedUserList.value = [...relatedUserList.value, ...response.data.results]
      relatedUserListNextURL.value = response.data.next
      done('ok')
    } catch (error) {
      console.error(error)
      done('error')
    }
  } else {
    done('empty')
  }
}

const createChat = async () => {
  chatCreating.value = true

  let formData = new FormData()
  formData.append('chat_type', selectedChatType.value)

  if (selectedChatType.value === chatType.DIALOG) {
    formData.append('members', selectedMembers.value[0])
  } else if (selectedChatType.value === chatType.GROUP) {
    selectedMembers.value.forEach((element) => {
      formData.append('members', element)
    })
    formData.append('name', groupChatName.value)
    if (groupChatImage.value) {
      formData.append('image', groupChatImage.value)
    }
  }

  try {
    const response = await axios.post('/messenger/chat/create/', formData)
    if (response.status === 201) {
      createChatDialog.value = false
      selectedChatType.value = chatType.DIALOG
      selectedMembers.value = []
      groupChatName.value = ''
      groupChatImage.value = null
      relatedUserList.value = []
      relatedUserListNextURL.value = null
      errors.value = null
    }
  } catch (error) {
    if (error.response.data.uuid) {
      router.push({
        name: 'Chat',
        params: { uuid: error.response.data.uuid }
      })
      createChatDialog.value = false
    } else {
      errors.value = error.response.data
    }
  } finally {
    chatCreating.value = false
  }
}

const changeSelectedMembers = (user_uuid) => {
  if (selectedChatType.value === chatType.DIALOG) {
    selectedMembers.value = [user_uuid]
  } else if (selectedChatType.value === chatType.GROUP) {
    if (selectedMembers.value.includes(user_uuid)) {
      selectedMembers.value = selectedMembers.value.filter((element) => {
        return element !== user_uuid
      })
    } else {
      selectedMembers.value.push(user_uuid)
    }
  }
}

const updateUserStatus = (mutation, state) => {
  chatList.value.forEach((element) => {
    if (
      element.chat_type === chatType.DIALOG &&
      element.details.uuid === state.user_uuid
    ) {
      element.details.status = state.status
    }
  })
}

watch(selectedChatType, () => {
  selectedMembers.value = []
  groupChatName.value = ''
  groupChatImage.value = null
  errors.value = null
})

onMounted(async () => {
  await getChatList()
  connectionBusStore.$subscribe(updateUserStatus)
})

onUnmounted(() => {
  closeChatListSocket()
})
</script>

<template>
  <v-container>
    <v-row class="border rounded-lg elevation-1">
      <v-col
        :cols="12"
        :md="4"
      >
        <div class="d-flex justify-space-evenly d-md-none">
          <v-btn
            @click.stop="chatListDrawer = true"
            variant="tonal"
            prepend-icon="mdi-format-list-bulleted"
          >
            {{ $t('messenger.chat_list') }}
          </v-btn>
          <v-navigation-drawer
            v-model="chatListDrawer"
            location="start"
            temporary
          >
            <div
              v-if="chatListLoading"
              class="d-flex justify-center align-center my-10"
            >
              <v-progress-circular
                indeterminate
                :size="50"
              ></v-progress-circular>
            </div>

            <v-infinite-scroll
              v-else-if="chatList.length > 0"
              @load="getMoreChatList"
              mode="intersect"
              empty-text="&nbsp;"
            >
              <ChatList :chatList="chatList" />
            </v-infinite-scroll>

            <v-alert
              v-else
              type="info"
              variant="tonal"
              class="my-5"
            >
              {{ $t('messenger.no_chats') }}
            </v-alert>
          </v-navigation-drawer>

          <v-btn
            @click="() => {
              getRelatedUserList()
              createChatDialog = true
            }"
            variant="tonal"
            append-icon="mdi-plus-circle-outline"
          >
            {{ $t('messenger.create_chat') }}
          </v-btn>
        </div>
        <div class="d-none d-md-block">
          <div class="d-flex justify-space-between align-center border-b-sm">
            <h2 class="text-h5">{{ $t('messenger.chats') }}</h2>
            <v-btn
              @click="() => {
                getRelatedUserList()
                createChatDialog = true
              }"
              variant="text"
              icon="mdi-plus-circle-outline"
            ></v-btn>
          </div>

          <div
            v-if="chatListLoading"
            class="d-flex justify-center align-center my-10"
          >
            <v-progress-circular
              indeterminate
              :size="50"
            ></v-progress-circular>
          </div>

          <v-infinite-scroll
            v-else-if="chatList.length > 0"
            @load="getMoreChatList"
            mode="intersect"
            height="73vh"
            empty-text="&nbsp;"
          >
            <ChatList :chatList="chatList" />
          </v-infinite-scroll>

          <v-alert
            v-else
            type="info"
            variant="tonal"
            class="my-5"
          >
            {{ $t('messenger.no_chats') }}
          </v-alert>
        </div>
      </v-col>
      <v-col
        :cols="12"
        :md="8"
      >
        <router-view
          @msgViewed="chatList[chatIndex].unviewed_msg_count -= 1"
          @leaveChat="(chatUUID) => {
            chatList = chatList.filter((element) => {
              return element.uuid !== chatUUID
            })
          }"
        />
      </v-col>
    </v-row>
  </v-container>

  <v-dialog
    v-model="createChatDialog"
    :width="500"
    persistent
  >
    <v-card
      rounded="lg"
      :title="$t('messenger.creating_chat')"
    >
      <div class="text-center my-3">
        <v-btn-toggle v-model="selectedChatType">
          <v-btn :value="chatType.DIALOG">
            {{ $t('messenger.dialog') }}
          </v-btn>
          <v-btn :value="chatType.GROUP">
            {{ $t('messenger.group') }}
          </v-btn>
        </v-btn-toggle>
      </div>

      <div
        v-if="selectedChatType === chatType.GROUP"
        class="mx-3"
      >
        <v-text-field
          v-model="groupChatName"
          :readonly="chatCreating"
          type="text"
          maxlength="150"
          variant="filled"
          :label="$t('messenger.group_name')"
          :error-messages="errors?.name ? errors.name : []"
        ></v-text-field>

        <span v-if="groupChatImage">
          {{ $t('messenger.chosen_image') }}:
          {{ groupChatImage.name }}
        </span>
        <FileInputButton
          @selectedFiles="(filelist) => groupChatImage = filelist[0]"
          accept="image/*"
          variant="tonal"
          color="primary"
          block
          class="text-none"
          :text="$t('messenger.choose_image')"
        ></FileInputButton>
        <div
          v-if="errors && errors.image"
          class="text-error"
        >
          <small v-for="error in errors.image">
            {{ error }}
          </small>
        </div>
      </div>

      <div
        v-if="relatedUserListLoading"
        class="d-flex justify-center align-center my-10"
      >
        <v-progress-circular
          indeterminate
          :size="50"
        ></v-progress-circular>
      </div>

      <v-infinite-scroll
        v-else-if="relatedUserList.length > 0"
        @load="getMoreRelatedUserList"
        mode="intersect"
        :max-height="500"
        empty-text="&nbsp;"
      >
        <v-list class="mx-3">
          <v-list-item
            v-for="user in relatedUserList"
            :key="user.uuid"
          >
            <template v-slot:prepend>
              <AvatarExtended
                :image="user.avatar"
                :size="32"
                :online="user.status === 'online' ? true : false"
              />
            </template>
            <template v-slot:title>
              <span class="text-subtitle-1 font-weight-medium mx-3">
                {{ user.name }}
              </span>
            </template>
            <template v-slot:append>
              <v-list-item-action>
                <input
                  :value="user.uuid"
                  :checked="selectedMembers.includes(user.uuid)"
                  @change="changeSelectedMembers(user.uuid)"
                  :type="selectedChatType === chatType.DIALOG ? 'radio' : 'checkbox'"
                >
              </v-list-item-action>
            </template>
          </v-list-item>
        </v-list>
      </v-infinite-scroll>

      <v-alert
        v-else
        type="info"
        variant="tonal"
        class="my-5 mx-3"
      >
        {{ $t('follow.no_followers_and_following') }}
      </v-alert>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            createChatDialog = false
            selectedChatType = chatType.DIALOG
            selectedMembers = []
            groupChatName = ''
            groupChatImage = null
            relatedUserList = []
            relatedUserListNextURL = null
            errors = null
          }"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="createChat()"
          :loading="chatCreating"
          :disabled="chatCreationDisabled"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.create') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 0.3em;
}

input[type="radio"],
input[type="checkbox"] {
  width: 1.15em;
  height: 1.15em;
  accent-color: black;
}
input[type="radio"]:hover,
input[type="checkbox"]:hover {
  cursor: pointer;
}

.v-col-12.v-col-md-4 {
  border-bottom: 1px solid #dee2e6;
}
@media(min-width: 960px) {
  .v-col-12.v-col-md-4 {
    border-bottom: none;
    border-right: 1px solid #dee2e6;
  }
}
</style>
