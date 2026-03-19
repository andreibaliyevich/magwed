<script setup>
defineProps({
  msgContent: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div style="white-space: pre-line;">
    {{ msgContent }}
  </div>
</template>
