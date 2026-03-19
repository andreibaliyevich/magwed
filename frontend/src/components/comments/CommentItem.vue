<script setup>
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useSendComment } from '@/composables/sendComment.js'
import ReportListItemDialog from '../ReportListItemDialog.vue'

const userStore = useUserStore()

const props = defineProps({
  commentItem: {
    type: Object,
    required: true
  }
})

const replyComment = ref(false)
const {
  newCommentSending,
  newCommentContent,
  newCommentErrors,
  sendComment
} = useSendComment('comment', props.commentItem.uuid)

const { getLocaleDateTimeString } = useLocaleDateTime()

watch(newCommentContent, (newValue) => {
  if (!newValue) {
    replyComment.value = false
  }
})
</script>

<template>
  <div class="d-flex ga-3">
    <router-link
      v-if="commentItem.author.profile_url"
      :to="{
        name: 'OrganizerDetail',
        params: { profile_url: commentItem.author.profile_url }
      }"
    >
      <AvatarExtended
        :image="commentItem.author.avatar"
        :size="32"
        :online="commentItem.author.status === 'online' ? true : false"
      />
    </router-link>
    <AvatarExtended
      v-else
      :image="commentItem.author.avatar"
      :size="32"
      :online="commentItem.author.status === 'online' ? true : false"
    />

    <div class="flex-grow-1">
      <div class="d-flex justify-space-between">
        <router-link
          v-if="commentItem.author.profile_url"
          :to="{
            name: 'OrganizerDetail',
            params: { profile_url: commentItem.author.profile_url }
          }"
          class="text-decoration-none text-black"
        >
          <strong>{{ commentItem.author.name }}</strong>
        </router-link>
        <strong v-else>
          {{ commentItem.author.name }}
        </strong>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(commentItem.created_at) }}
        </small>
      </div>

      <div class="d-flex justify-space-between">
        <div style="white-space: pre-line;">
          {{ commentItem.content }}
        </div>
        <v-menu
          v-if="userStore.isLoggedIn"
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
          <template v-slot:default="{ isActive }">
            <v-list density="compact">
              <v-list-item
                @click="() => {
                  isActive.value = false
                  replyComment = true
                }"
                prepend-icon="mdi-reply"
              >
                {{ $t('btn.reply') }}
              </v-list-item>
              <ReportListItemDialog
                contentType="comment"
                :objectUUID="commentItem.uuid"
                @reportSent="isActive.value = false"
              />
            </v-list>
          </template>
        </v-menu>
      </div>

      <v-textarea
        v-if="replyComment"
        v-model="newCommentContent"
        :loading="newCommentSending"
        :readonly="newCommentSending"
        :append-inner-icon="newCommentContent ? 'mdi-send' : ''"
        @click:append-inner="sendComment()"
        :rows="1"
        :max-rows="10"
        auto-grow
        autofocus
        variant="solo-filled"
        flat
        :placeholder="$t('comments.add_comment')"
        :error-messages="newCommentErrors?.content ? newCommentErrors.content : []"
      ></v-textarea>
    </div>
  </div>
</template>
