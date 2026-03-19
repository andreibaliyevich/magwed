import axios from 'axios'
import { ref } from 'vue'

export function useSendComment(content_type, object_uuid) {
  const newCommentSending = ref(false)
  const newCommentContent = ref('')
  const newCommentErrors = ref(null)

  const sendComment = async () => {
    newCommentSending.value = true
    try {
      const response = await axios.post('/comments/', {
        content_type: content_type,
        object_uuid: object_uuid,
        content: newCommentContent.value
      })
      newCommentContent.value = ''
      newCommentErrors.value = null
    } catch (error) {
      newCommentErrors.value = error.response.data
    } finally {
      newCommentSending.value = false
    }
  }

  return {
    newCommentSending,
    newCommentContent,
    newCommentErrors,
    sendComment,
  }
}
