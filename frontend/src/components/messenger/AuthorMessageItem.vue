<script setup>
import { messageType } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import TextMessage from './TextMessage.vue'
import ImageMessage from './ImageMessage.vue'
import FileMessage from './FileMessage.vue'

defineProps({
  msg: {
    type: Object,
    required: true
  }
})

const { getLocaleDateTimeString } = useLocaleDateTime()
</script>

<template>
  <div class="d-flex align-end flex-column">
    <v-sheet
      max-width="30rem"
      rounded
      color="blue"
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
      <div class="d-flex justify-end">
        <v-icon
          :icon="msg.viewed_by.length ? 'mdi-check-all' : 'mdi-check'"
          :size="16"
        ></v-icon>
      </div>
    </v-sheet>
    <small class="text-secondary">
      {{ getLocaleDateTimeString(msg.created_at) }}
    </small>
  </div>
</template>