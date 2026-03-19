<script setup>
import axios from 'axios'
import { ref } from 'vue'

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
const emit = defineEmits(['reportSent'])

const reportSending = ref(false)
const reportComment = ref('')
const sendReportDialog = ref(false)
const errors = ref(null)

const sendReport = async () => {
  reportSending.value = true
  try {
    const response = await axios.post('/support/report/', {
      content_type: props.contentType,
      object_uuid: props.objectUUID,
      comment: reportComment.value
    })
    if (response.status === 201) {
      errors.value = null
      sendReportDialog.value = false
      reportComment.value = ''
      emit('reportSent')
    }
  } catch (error) {
    errors.value = error.response.data
  } finally {
    reportSending.value = false
  }
}
</script>

<template>
  <v-list-item
    @click="sendReportDialog = true"
    prepend-icon="mdi-flag"
  >
    {{ $t('report.report') }}
  </v-list-item>

  <v-dialog
    :model-value="sendReportDialog"
    :width="500"
  >
    <v-card
      :title="$t('report.new_report')"
      rounded="lg"
    >
      <v-textarea
        v-model="reportComment"
        :readonly="reportSending"
        autofocus
        auto-grow
        :rows="5"
        :max-rows="10"
        variant="filled"
        :label="$t('report.comment')"
        :error-messages="errors?.comment ? errors.comment : []"
        class="mt-3 mx-3"
      ></v-textarea>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="sendReportDialog = false">
          {{ $t('btn.cancel') }}
        </v-btn>
        <v-btn
          @click="sendReport()"
          :loading="reportSending"
          :disabled="!reportComment"
          variant="flat"
          color="primary"
        >
          {{ $t('btn.send') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
