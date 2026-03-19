<script>
export default {
  name: 'FileDropZoneInputButton',
  inheritAttrs: false,
  props: {
    buttonText: {
      type: String,
      required: true
    },
    zoneText: {
      type: String,
      required: true
    }
  },
  methods: {
    dropHandler(event) {
      const filelist = [...event.dataTransfer.files]
      this.$emit('selectedFiles', filelist)
      this.$refs.dropArea.classList.remove('drop-area-over')
    },
    changeInput(event) {
      const filelist = [...event.target.files]
      this.$emit('selectedFiles', filelist)
      event.target.value = null
    }
  }
}
</script>

<template>
  <div
    ref="dropArea"
    @dragover.prevent="$refs.dropArea.classList.add('drop-area-over')"
    @dragleave.prevent="$refs.dropArea.classList.remove('drop-area-over')"
    @drop.prevent="dropHandler"
    class="d-flex justify-center align-center rounded-lg pa-5"
  >
    <div class="text-center">
      <v-icon
        icon="mdi-cloud-upload-outline"
        :size="48"
      ></v-icon>
      <div class="px-2 my-2">{{ zoneText }}</div>
      <input
        ref="fileInput"
        @change="changeInput"
        type="file"
        v-bind="$attrs"
        class="hidden-visually"
      >
      <v-btn
        @click.stop="$refs.fileInput.click()"
        :text="buttonText"
        variant="tonal"
        color="primary"
        class="text-none"
        append-icon="mdi-upload"
      ></v-btn>
    </div>
  </div>
</template>

<style scoped>
.d-flex.justify-center.align-center.rounded-lg.pa-5 {
  width: 100%;
  background-color: #f8f9fa;
  border-width: 3px;
  border-style: dashed;
  border-color: #adb5bd;
}
.drop-area-over {
  background-color: #e2e3e5 !important;
  border-style: solid !important;
  border-color: #e72a26 !important;
}
</style>
