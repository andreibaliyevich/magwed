<script setup>
import axios from 'axios'
import { ref, onMounted, onUnmounted } from 'vue'
import { WS_URL } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import { useConnectionBusStore } from '@/stores/connectionBus.js'
import { useSendComment } from '@/composables/sendComment.js'
import AuthorCommentItem from './AuthorCommentItem.vue'
import CommentItem from './CommentItem.vue'

const userStore = useUserStore()
const connectionBusStore = useConnectionBusStore()

const props = defineProps({
  contentType: {
    type: String,
    required: true
  },
  objectUUID: {
    type: String,
    required: true
  }
})

const commentListLoading = ref(true)
const commentList = ref([])
const commentCount = ref(0)
const nextURL = ref(null)

const commentSocket = ref(null)
const commentSocketConnect = ref(false)

const {
  newCommentSending,
  newCommentContent,
  newCommentErrors,
  sendComment
} = useSendComment(props.contentType, props.objectUUID)

const getCommentList = async () => {
  try {
    const response = await axios.get('/comments/', {
      params: {
        content_type__model: props.contentType,
        object_uuid: props.objectUUID
      }
    })
    commentList.value = response.data.results
    commentCount.value = response.data.count
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    commentListLoading.value = false
  }
}

const getMoreCommentList = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      commentList.value = [...commentList.value, ...response.data.results]
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

const getCommentListOfComment = (inList) => {
  let outList = []
  for (let i = 0; i < inList.length; i++) {
    outList.push(inList[i])

    if (inList[i].comments.length > 0) {
      outList.push(...getCommentListOfComment(inList[i].comments))
    }
  }
  return outList
}

const addCommentToList = (cList, data) => {
  for (let i = 0; i < cList.length; i++) {
    if (cList[i].uuid === data.comment_uuid) {
      cList[i].comments.push(data.instance)
      return true
    } else if (cList[i].comments.length > 0) {
      const result = addCommentToList(cList[i].comments, data)
      if (result) {
        return true
      }
    }
  }
  return false
}

const updateCommentFromList = (cList, data) => {
  for (let i = 0; i < cList.length; i++) {
    if (cList[i].uuid === data.uuid) {
      cList[i].content = data.content
      return true
    } else if (cList[i].comments.length > 0) {
      const result = updateCommentFromList(cList[i].comments, data)
      if (result) {
        return true
      }
    }
  }
  return false
}

const removeCommentFromList = (cList, data) => {
  for (let i = 0; i < cList.length; i++) {
    if (cList[i].uuid === data) {
      return [true, true]
    } else if (cList[i].comments.length > 0) {
      const result = removeCommentFromList(cList[i].comments, data)
      if (result[0]) {
        if (result[1]) {
          cList[i].comments = cList[i].comments.filter((element) => {
            return element.uuid !== data
          })
          return [true, false]
        } else {
          return [true, false]
        }
      }
    }
  }
  return [false, false]
}

const openCommentSocket = () => {
  commentSocket.value = new WebSocket(
    WS_URL
      + '/ws/comments/'
      + props.contentType
      + '/'
      + props.objectUUID
      + '/'
  )
  commentSocket.value.onopen = (event) => {
    commentSocketConnect.value = true
  }
  commentSocket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.action === 'create') {
      if (!!data.data.comment_uuid) {
        addCommentToList(commentList.value, data.data)
      } else {
        commentList.value.push(data.data.instance)
        commentCount.value += 1
      }
    } else if (data.action === 'update') {
      updateCommentFromList(commentList.value, data.data)
    } else if (data.action === 'destroy') {
      const result = removeCommentFromList(commentList.value, data.data)
      if (result[0] && result[1]) {
        commentList.value = commentList.value.filter((element) => {
          return element.uuid !== data.data
        })
        commentCount.value -= 1
      }
    }
  }
  commentSocket.value.onclose = (event) => {
    commentSocket.value = null
    commentSocketConnect.value = false
  }
  commentSocket.value.onerror = (error) => {
    commentSocket.value = null
    commentSocketConnect.value = false
  }
}

const closeCommentSocket = () => {
  if (commentSocket.value) {
    commentSocket.value.close()
  }
}

const updateUserStatus = (cList, state) => {
  cList.forEach((element) => {
    if (element.author.uuid === state.user_uuid) {
      element.author.status = state.status
    }
    if (element.comments.length > 0) {
      updateUserStatus(element.comments, state)
    }
  })
}

onMounted(async () => {
  await getCommentList()
  openCommentSocket()
  connectionBusStore.$subscribe((mutation, state) => {
    updateUserStatus(commentList.value, state)
  })
})

onUnmounted(() => {
  closeCommentSocket()
})
</script>

<template>
  <h6 class="text-h6 text-center my-5">
    {{ $t('comments.comments') }} ({{ commentCount }})
  </h6>

  <div
    v-if="commentListLoading"
    class="d-flex justify-center align-center my-15"
  >
    <v-progress-circular
      indeterminate
      :size="50"
    ></v-progress-circular>
  </div>

  <v-infinite-scroll
    v-else-if="commentList.length > 0"
    @load="getMoreCommentList"
    mode="intersect"
    empty-text="&nbsp;"
  >
    <TransitionGroup
      tag="ul"
      name="list-group"
      class="list-group"
    >
      <li
        v-for="commentItem in commentList"
        :key="commentItem.uuid"
        class="d-block my-3"
      >
        <AuthorCommentItem
          v-if="commentItem.author.uuid === userStore.uuid"
          :commentItem="commentItem"
        />
        <CommentItem
          v-else
          :commentItem="commentItem"
        />
        <TransitionGroup
          v-if="commentItem.comments.length > 0"
          tag="ul"
          name="list-group"
          class="list-group"
        >
          <li
            v-for="commentOfCommentItem in getCommentListOfComment(commentItem.comments)"
            :key="commentOfCommentItem.uuid"
            class="d-block my-3 mx-5"
          >
            <AuthorCommentItem
              v-if="commentOfCommentItem.author.uuid === userStore.uuid"
              :commentItem="commentOfCommentItem"
            />
            <CommentItem
              v-else
              :commentItem="commentOfCommentItem"
            />
          </li>
        </TransitionGroup>
      </li>
    </TransitionGroup>
  </v-infinite-scroll>

  <p
    v-else
    class="text-body-1 mx-1 my-5"
  >
    {{ $t('comments.no_comments_yet') }}
  </p>

  <v-textarea
    v-if="userStore.isLoggedIn"
    v-model="newCommentContent"
    :loading="newCommentSending"
    :readonly="newCommentSending"
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

  <v-alert
    v-else
    type="info"
    variant="tonal"
    class="my-5"
  >
    {{ $t('comments.need_log_in') }}
    <router-link
      :to="{
        name: 'Login',
        query: { redirect: $route.path }
      }"
      class="font-weight-bold"
    >
      {{ $t('auth.log_in') }}
    </router-link>
  </v-alert>
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
  transform: translateY(30px);
}
.list-group-leave-active {
  position: absolute;
}
</style>
