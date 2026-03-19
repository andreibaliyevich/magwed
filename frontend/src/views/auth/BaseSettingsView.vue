<script setup>
import { ref } from 'vue'
import SettingsMenu from '@/components/auth/SettingsMenu.vue'

const settingsMenuDrawer = ref(false)
</script>

<template>
  <v-container>
    <v-row>
      <v-col
        :cols="12"
        :md="3"
        class="border-right-md"
      >
        <v-btn
          @click.stop="settingsMenuDrawer = !settingsMenuDrawer"
          append-icon="mdi-dots-vertical"
          variant="outlined"
          block
          class="d-inline-flex d-md-none"
        >
          {{ $t('auth.settings_menu') }}
        </v-btn>
        <v-navigation-drawer
          v-model="settingsMenuDrawer"
          location="end"
          temporary
        >
          <SettingsMenu drawer />
        </v-navigation-drawer>
        <SettingsMenu />
      </v-col>
      <v-col
        :cols="12"
        :md="9"
        class="px-md-12"
      >
        <router-view />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
@media(min-width: 960px) {
  .border-right-md {
    border-right: 1px solid #BDBDBD;
  }
}
</style>
