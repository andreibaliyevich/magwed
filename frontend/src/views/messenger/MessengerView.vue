<template>
  <v-sheet
    height="100%"
    min-height="75vh"
    class="d-flex flex-column justify-center align-center"
  >
    <v-icon
      icon="mdi-chat-outline"
      :size="150"
      color="secondary"
    ></v-icon>
    <p class="text-h5 mt-3">{{ $t('messenger.select_chat') }}</p>
  </v-sheet>
</template>
