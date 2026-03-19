<script setup>
import { userType } from '@/config.js'
import { useUserStore } from '@/stores/user.js'
import { useLogout } from '@/composables/logout.js'

const userStore = useUserStore()
const { logout } = useLogout()

defineProps({
  drawer: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <v-list :class="{ 'd-none d-md-block position-sticky': !drawer }">
    <v-list-item>
      <div class="d-flex justify-center">
        <v-avatar :size="128">
          <v-img
            v-if="userStore.avatar"
            :src="userStore.avatar"
            :alt="userStore.name"
          ></v-img>
          <v-icon
            v-else
            icon="mdi-account-circle"
            :size="128"
            role="img"
          ></v-icon>
        </v-avatar>
      </div>
    </v-list-item>
    <v-list-item>
      <template v-slot:title>
        <div class="text-center">{{ userStore.name }}</div>
      </template>
      <template v-slot:subtitle>
        <div class="text-center">{{ userStore.email }}</div>
      </template>
    </v-list-item>
    <v-list-item
      :to="{ name: 'Profile' }"
      :active="$route.name === 'Profile'"
      prepend-icon="mdi-account-edit-outline"
    >
      <v-list-item-title>
        {{ $t('user.profile') }}
      </v-list-item-title>
    </v-list-item>
    <v-list-item
      v-if="userStore.userType === userType.ORGANIZER"
      :to="{ name: 'SocialLinks' }"
      :active="$route.name === 'SocialLinks'"
      prepend-icon="mdi-link-variant"
    >
      <v-list-item-title>
        {{ $t('auth.sociallinks.social_links') }}
      </v-list-item-title>
    </v-list-item>
    <v-list-item
      v-if="userStore.userType === userType.ORGANIZER"
      :to="{ name: 'Portfolio' }"
      :active="
        $route.name === 'Portfolio'
          || $route.name === 'PortfolioAlbumList'
          || $route.name === 'PortfolioAlbumDetail'
          || $route.name === 'PortfolioPhotoList'
      "
      prepend-icon="mdi-briefcase-outline"
    >
      <v-list-item-title>
        {{ $t('portfolio.portfolio') }}
      </v-list-item-title>
    </v-list-item>
    <v-list-item
      :to="{ name: 'PasswordChange' }"
      :active="$route.name === 'PasswordChange'"
      prepend-icon="mdi-key-outline"
    >
      <v-list-item-title>
        {{ $t('auth.passwordchange.password_change') }}
      </v-list-item-title>
    </v-list-item>
    <v-list-item
      :to="{ name: 'ProfileDelete' }"
      :active="$route.name === 'ProfileDelete'"
      prepend-icon="mdi-account-remove-outline"
    >
      <v-list-item-title>
        {{ $t('auth.profile_delete.profile_delete') }}
      </v-list-item-title>
    </v-list-item>
    <v-list-item
      @click="logout()"
      prepend-icon="mdi-logout"
    >
      <v-list-item-title>
        {{ $t('auth.log_out') }}
      </v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<style scoped>
.d-none.d-md-block.position-sticky {
  top: 64px;
}
</style>
