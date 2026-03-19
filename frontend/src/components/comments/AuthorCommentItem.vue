<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import { useSendComment } from '@/composables/sendComment.js'
import ReportListItemDialog from '../ReportListItemDialog.vue'

const props = defineProps({
  commentItem: {
    type: Object,
    required: true
  }
})

const oldCommentProcessing = ref(false)
const oldCommentContent = ref('')
const oldCommentErrors = ref(null)

const replyComment = ref(false)
const {
  newCommentSending,
  newCommentContent,
  newCommentErrors,
  sendComment
} = useSendComment('comment', props.commentItem.uuid)

const { getLocaleDateTimeString } = useLocaleDateTime()

const commentMenu = ref(false)
const commentUpdateDialog = ref(false)
const commentRemoveDialog = ref(false)

const updateComment = async () => {
  oldCommentProcessing.value = true
  try {
    const response = await axios.put(
      '/comments/'
        + props.commentItem.uuid
        +'/',
      { content: oldCommentContent.value }
    )
    if (response.status === 200) {
      commentUpdateDialog.value = false
      commentMenu.value = false
      oldCommentContent.value = ''
      oldCommentErrors.value = null
    }
  } catch (error) {
    oldCommentErrors.value = error.response.data
  } finally {
    oldCommentProcessing.value = false
  }
}

const removeComment = async () => {
  oldCommentProcessing.value = true
  try {
    const response = await axios.delete(
      '/comments/'
        + props.commentItem.uuid
        +'/'
    )
    if (response.status === 204) {
      commentRemoveDialog.value = false
      commentMenu.value = false
    }
  } catch (error) {
    console.error(error)
  } finally {
    oldCommentProcessing.value = false
  }
}

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
          v-model="commentMenu"
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
          <v-list density="compact">
            <v-list-item
              @click="() => {
                commentMenu = false
                replyComment = true
              }"
              prepend-icon="mdi-reply"
            >
              {{ $t('btn.reply') }}
            </v-list-item>
            <ReportListItemDialog
              contentType="comment"
              :objectUUID="commentItem.uuid"
              @reportSent="commentMenu = false"
            />
            <v-list-item
              @click="() => {
                oldCommentContent = commentItem.content
                commentUpdateDialog = true
              }"
              prepend-icon="mdi-pencil"
            >
              {{ $t('btn.edit') }}
            </v-list-item>
            <v-list-item
              @click="commentRemoveDialog = true"
              prepend-icon="mdi-delete"
            >
              {{ $t('btn.delete') }}
            </v-list-item>
          </v-list>
        </v-menu>
      </div>

      <v-textarea
        v-if="replyComment"
        v-model="newCommentContent"
        :loading="newCommentSending"
        :readonly="newCommentSending"
        autofocus
        auto-grow
        :rows="1"
        :max-rows="10"
        variant="solo-filled"
        flat
        :placeholder="$t('comments.add_comment')"
        :append-inner-icon="newCommentContent ? 'mdi-send' : ''"
        @click:append-inner="sendComment()"
        :error-messages="newCommentErrors?.content ? newCommentErrors.content : []"
      ></v-textarea>
    </div>
  </div>

  <v-dialog
    :model-value="commentUpdateDialog"
    :width="500"
    persistent
  >
    <v-card
      :title="$t('comments.updating_comment')"
      rounded="lg"
    >
      <v-textarea
        v-model="oldCommentContent"
        :readonly="oldCommentProcessing"
        autofocus
        auto-grow
        :rows="1"
        :max-rows="10"
        variant="filled"
        :label="$t('comments.content')"
        :error-messages="oldCommentErrors?.content ? oldCommentErrors.content : []"
        class="mt-3 mx-3"
      ></v-textarea>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="() => {
            commentUpdateDialog = false
            oldCommentContent = ''
            oldCommentErrors = null
          }"
        >
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="updateComment()"
          :loading="oldCommentProcessing"
          :disabled="!oldCommentContent"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.update') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    :model-value="commentRemoveDialog"
    width="auto"
    persistent
  >
    <v-card rounded="lg">
      <v-card-title>
        {{ $t('comments.you_want_remove_comment') }}
      </v-card-title>
      <v-card-text>
        {{ $t('comments.you_can_update_this_comment') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="commentRemoveDialog = false">
          {{ $t('btn.no_cancel') }}
        </v-btn>
        <v-btn
          @click="removeComment()"
          :loading="oldCommentProcessing"
        >
          <strong>{{ $t('btn.yes_i_am_sure') }}</strong>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
