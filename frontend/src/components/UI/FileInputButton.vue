<script>
export default {
  name: 'FileInputButton',
  inheritAttrs: false,
  props: {
    accept: {
      type: String,
      default: '*/*'
    },
    multiple: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    changeInput(event) {
      const filelist = [...event.target.files]
      this.$emit('selectedFiles', filelist)
      event.target.value = null
    }
  }
}
</script>

<template>
  <input
    ref="fileInput"
    @change="changeInput"
    type="file"
    :accept="accept"
    :multiple="multiple"
    class="hidden-visually"
  >
  <v-btn
    @click.stop="$refs.fileInput.click()"
    v-bind="$attrs"
  ></v-btn>
</template>
