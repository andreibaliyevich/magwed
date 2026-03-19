<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  msgContent: {
    type: Object,
    required: true
  }
})

const imgOverlay = ref(false)
const imgUuid = ref(null)

const imgIndex = computed(() => {
  return props.msgContent.findIndex((element) => {
    return element.uuid === imgUuid.value
  })
})
</script>

<template>
  <ul
    style="
      max-width: 30rem;
      list-style: none;
      line-height: 0;
    "
  >
    <li
      v-for="img in msgContent"
      style="
        display: inline-flex;
        margin: 1px;
      "
    >
      <v-img
        :src="img.content"
        :width="150"
        :aspect-ratio="1/1"
        cover
        @click="() => {
          imgUuid = img.uuid
          imgOverlay = true
        }"
        class="cursor-pointer"
      ></v-img>
    </li>
  </ul>

  <v-overlay
    v-model="imgOverlay"
    width="100vw"
    height="100vh"
    :opacity="0.5"
    content-class="d-flex justify-center align-center"
  >
    <v-img
      :src="msgContent[imgIndex]?.content"
      max-width="100%"
      max-height="100vh"
    ></v-img>
    <v-btn
      @click="() => {
        imgOverlay = false
        imgUuid = null
      }"
      icon="mdi-close"
      :size="48"
      :elevation="1"
      style="
        position: absolute;
        top: 4px;
        right: 12px;
      "
    ></v-btn>
    <v-btn
      @click="imgUuid = msgContent[imgIndex - 1].uuid"
      :disabled="imgIndex === 0"
      icon="mdi-chevron-left"
      :size="48"
      :elevation="1"
      style="
        position: absolute;
        top: 50%;
        left: 12px;
        transform: translateY(-50%);
      "
    ></v-btn>
    <v-btn
      @click="imgUuid = msgContent[imgIndex + 1].uuid"
      :disabled="imgIndex === msgContent.length - 1"
      icon="mdi-chevron-right"
      :size="48"
      :elevation="1"
      style="
        position: absolute;
        top: 50%;
        right: 12px;
        transform: translateY(-50%);
      "
    ></v-btn>
  </v-overlay>
</template>
