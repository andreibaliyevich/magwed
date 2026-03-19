<script setup>
import { chatType, messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import TextMessage from './TextMessage.vue'
import ImageMessage from './ImageMessage.vue'
import FileMessage from './FileMessage.vue'

defineProps({
  chatTypeData: {
    type: Number,
    required: true
  },
  msg: {
    type: Object,
    required: true
  }
})

const { getLocaleDateTimeString } = useLocaleDateTime()
</script>

<template>
  <div
    :data-uuid="msg.uuid"
    class="d-flex align-start flex-column"
  >
    <v-sheet
      v-if="chatTypeData === chatType.DIALOG"
      max-width="30rem"
      rounded
      color="grey-lighten-5"
      class="pa-1"
    >
      <TextMessage
        v-if="msg.msg_type === messageType.TEXT"
        :msgContent="msg.content"
      />
      <ImageMessage
        v-else-if="msg.msg_type === messageType.IMAGES"
        :msgContent="msg.content"
      />
      <FileMessage
        v-else-if="msg.msg_type === messageType.FILES"
        :msgContent="msg.content"
      />
    </v-sheet>
    <div
      v-else
      class="d-flex align-start ga-1"
    >
      <AvatarExtended
        :image="msg.author.avatar"
        :size="36"
        :online="msg.author.status === 'online' ? true : false"
      />
      <v-sheet
        max-width="30rem"
        rounded
        color="grey-lighten-5"
        class="pa-1"
      >
        <p class="font-weight-bold mb-0">{{ msg.author.name }}</p>
        <TextMessage
          v-if="msg.msg_type === messageType.TEXT"
          :msgContent="msg.content"
        />
        <ImageMessage
          v-else-if="msg.msg_type === messageType.IMAGES"
          :msgContent="msg.content"
        />
        <FileMessage
          v-else-if="msg.msg_type === messageType.FILES"
          :msgContent="msg.content"
        />
      </v-sheet>
    </div>
    <small class="text-secondary">
      {{ getLocaleDateTimeString(msg.created_at) }}
    </small>
  </div>
</template>