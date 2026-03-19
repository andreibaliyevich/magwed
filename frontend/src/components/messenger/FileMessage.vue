<script setup>
defineProps({
  msgContent: {
    type: Object,
    required: true
  }
})

const getName = (path) => {
  return path.split('/').at(-1)
}

const getSize = (value) => {
  if (value === 0) return '0 Bytes'
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(value) / Math.log(1024))
  return parseFloat((value / Math.pow(1024, i)).toFixed(1)) + ' ' + sizes[i]
}
</script>

<template>
  <ul
    style="
      max-width: 30rem;
      list-style: none;
    "
  >
    <li
      v-for="file in msgContent"
      style="margin: 1px;"
    >
      <div class="d-flex align-center ga-1">
        <v-btn
          :href="file.content"
          target="_blank"
          variant="text"
          icon="mdi-arrow-down-circle"
        ></v-btn>
        <div class="d-inline-block">
          <p class="font-weight-medium">{{ getName(file.content) }}</p>
          <small class="text-medium-emphasis">{{ getSize(file.size) }}</small>
        </div>
      </div>
    </li>
  </ul>
</template>
