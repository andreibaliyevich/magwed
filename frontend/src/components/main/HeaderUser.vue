<script setup>
import { userType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import { useLogout } from '@/composables/logout.js'

const userStore = useUserStore()
const { logout } = useLogout()
</script>

<template>
  <v-menu location="bottom end">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        icon
      >
        <v-avatar :size="32">
          <v-img
            v-if="userStore.avatar"
            :src="userStore.avatar"
            :alt="userStore.name"
          ></v-img>
          <v-icon
            v-else
            icon="mdi-account-circle"
            :size="32"
            role="img"
          ></v-icon>
        </v-avatar>
      </v-btn>
    </template>
    <v-sheet
      :min-width="210"
      :max-width="290"
      rounded="lg"
    >
      <v-list class="pb-0">
        <v-list-item>
          <template v-slot:prepend>
            <v-avatar :size="48">
              <v-img
                v-if="userStore.avatar"
                :src="userStore.avatar"
                :alt="userStore.name"
              ></v-img>
              <v-icon
                v-else
                icon="mdi-account-circle"
                :size="48"
                role="img"
              ></v-icon>
            </v-avatar>
          </template>
          <template v-slot:title>
            {{ userStore.name }}
          </template>
          <template v-slot:subtitle>
            {{ userStore.email }}
          </template>
        </v-list-item>
        <v-list-item>
          <v-btn
            :to="{
              name: 'Profile',
              params: { locale: $i18n.locale }
            }"
            :active="$route.name === 'Profile'"
            variant="tonal"
            color="primary"
            block
            class="text-none"
          >
            {{ $t('user.edit_profile') }}
          </v-btn>
        </v-list-item>
      </v-list>
      <v-list
        nav
        density="compact"
        class="pt-0"
      >
        <v-list-item
          :to="{
            name: 'Messenger',
            params: { locale: $i18n.locale }
          }"
          :active="
            $route.name === 'Messenger'
              || $route.name === 'Chat'
          "
          prepend-icon="mdi-message"
        >
          <v-list-item-title>
            {{ $t('messenger.messenger') }}
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          v-if="userStore.userType === userType.ORGANIZER"
          :to="{
            name: 'Followers',
            params: { locale: $i18n.locale }
          }"
          :active="$route.name === 'Followers'"
          prepend-icon="mdi-account-supervisor"
        >
          <v-list-item-title>
            {{ $t('follow.followers') }}
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          :to="{
            name: 'Following',
            params: { locale: $i18n.locale }
          }"
          :active="$route.name === 'Following'"
          prepend-icon="mdi-account-multiple"
        >
          <v-list-item-title>
            {{ $t('follow.following') }}
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          :to="{
            name: 'Favorites',
            params: { locale: $i18n.locale }
          }"
          :active="$route.name === 'Favorites'"
          prepend-icon="mdi-star"
        >
          <v-list-item-title>
            {{ $t('favorites.favorites') }}
          </v-list-item-title>
        </v-list-item>
        <v-divider class="my-1"></v-divider>
        <v-list-item
          @click="logout()"
          prepend-icon="mdi-logout"
        >
          <v-list-item-title>
            {{ $t('auth.log_out') }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-sheet>
  </v-menu>
</template>
