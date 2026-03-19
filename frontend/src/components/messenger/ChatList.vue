<script setup>
import { computed } from 'vue'
import { chatType, messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const props = defineProps({
  chatList: {
    type: Array,
    required: true
  }
})

const { getLocaleDateTimeString } = useLocaleDateTime()

const sortedChatList = computed(() => {
  return [...props.chatList].sort((chat1, chat2) => {
    return new Date(
      chat2.last_message?.created_at ? chat2.last_message.created_at : Date()
    ) - new Date(
      chat1.last_message?.created_at ? chat1.last_message.created_at : Date()
    )
  })
})
</script>

<template>
  <TransitionGroup
    tag="ul"
    name="list-group"
    class="list-group"
  >
    <li
      v-for="chat in sortedChatList"
      :key="chat.uuid"
    >
      <v-hover
        v-slot="{ isHovering, props }"
        :open-delay="100"
        :close-delay="100"
      >
        <router-link
          v-bind="props"
          :to="{
            name: 'Chat',
            params: { uuid: chat.uuid }
          }"
          :class="[
            'd-block rounded text-decoration-none pa-2',
            {
              'bg-grey-lighten-3': $route.params.uuid === chat.uuid,
              'bg-grey-lighten-4': isHovering
            }
          ]"
        >
          <div class="d-flex ga-3">
            <AvatarExtended
              v-if="chat.chat_type === chatType.DIALOG"
              :image="chat.details.avatar"
              :size="48"
              :online="chat.details.status === 'online' ? true : false"
            />
            <v-avatar
              v-else-if="chat.chat_type === chatType.GROUP"
              :image="chat.details.image ? chat.details.image : '/group-avatar.jpg'"
              :size="48"
            ></v-avatar>
            <v-avatar
              v-else
              image="/chat.jpg"
              :size="48"
            ></v-avatar>
            <div class="flex-grow-1">
              <div class="d-flex justify-space-between align-center text-black">
                <div
                  v-if="chat.chat_type === chatType.GROUP"
                  class="d-flex"
                >
                  <v-icon icon="mdi-account-group"></v-icon>
                  <strong class="ms-1">{{ chat.details.name }}</strong>
                </div>
                <strong v-else>
                  {{ chat.details.name }}
                </strong>
                <small v-if="chat.last_message">
                  {{ getLocaleDateTimeString(chat.last_message.created_at) }}
                </small>
              </div>
              <div
                v-if="chat.last_message"
                class="d-flex align-center"
              >
                <span
                  v-if="chat.last_message.msg_type === messageType.TEXT"
                  class="text-grey"
                >
                  {{ chat.last_message.content }}
                </span>
                <span
                  v-else-if="chat.last_message.msg_type === messageType.IMAGES"
                  class="text-grey"
                >
                  {{ $t('messenger.images', { n: chat.last_message.content }) }}
                </span>
                <span
                  v-else-if="chat.last_message.msg_type === messageType.FILES"
                  class="text-grey"
                >
                  {{ $t('messenger.files', { n: chat.last_message.content }) }}
                </span>
                <v-badge
                  v-if="chat.unviewed_msg_count > 0"
                  :content="chat.unviewed_msg_count"
                  inline
                  color="info"
                  class="ms-auto"
                ></v-badge>
              </div>
            </div>
          </div>
        </router-link>
      </v-hover>
    </li>
  </TransitionGroup>
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
  transform: translateY(-30px);
}
.list-group-leave-active {
  position: absolute;
}

strong,
small,
.text-grey {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
