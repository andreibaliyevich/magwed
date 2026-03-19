<script>
export default {
  name: 'AvatarExtended',
  inheritAttrs: false,
  props: {
    image: String,
    size: {
      type: Number,
      required: true
    },
    online: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    statusSize() {
      return parseInt((this.size / 33) + (116 / 11))
    },
    statusMargin() {
      return parseInt((this.size * 3 / 22) - (72 / 11))
    }
  }
}
</script>

<template>
  <div
    class="avatar-extended"
    :style="{
      'width': size + 'px',
      'height': size + 'px'
    }"
  >
    <v-avatar
      :image="image ? image : '/user-avatar.png'"
      :size="size"
      v-bind="$attrs"
    ></v-avatar>
    <span
      :class="[
        'status-indicator',
        online ? 'indicator-online' : 'indicator-offline'
      ]"
      :style="{
        'width': statusSize + 'px',
        'height': statusSize + 'px',
        'margin-right': statusMargin + 'px',
        'margin-bottom': statusMargin + 'px'
      }"
    ></span>
  </div>
</template>

<style scoped>
.avatar-extended {
  position: relative;
}
.status-indicator {
  position: absolute;
  bottom: 0;
  right: 0;
  border: 2px solid #f8f9fa;
  border-radius: 50%;
}
.indicator-online {
  background-color: #198754;
}
.indicator-offline {
  background-color: #6c757d;
}
</style>
