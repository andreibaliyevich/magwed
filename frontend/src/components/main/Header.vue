<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user.js'
import HeaderSearch from './HeaderSearch.vue'
import HeaderNotifications from './HeaderNotifications.vue'
import HeaderUser from './HeaderUser.vue'

const userStore = useUserStore()
const navDrawer = ref(false)
</script>

<template>
  <v-app-bar
    height="64"
    scroll-behavior="elevate"
    style="border-bottom: 1px solid #E0E0E0;"
  >
    <v-app-bar-nav-icon
      @click.stop="navDrawer = !navDrawer"
      variant="text"
      class="d-block d-md-none"
    ></v-app-bar-nav-icon>

    <v-container class="d-flex align-center">
      <router-link
        :to="{
          name: 'Home',
          params: { locale: $i18n.locale }
        }"
        class="me-5"
      >
        <img
          src="/logo-navbar.png"
          width="50"
          class="d-block d-sm-none"
        >
        <img
          src="/logo-navbar-full.png"
          width="150"
          class="d-none d-sm-block"
        >
      </router-link>

      <nav class="d-none d-md-flex align-center">
        <v-btn
          :to="{
            name: 'OrganizerList',
            params: { locale: $i18n.locale }
          }"
          :active="
            $route.name === 'OrganizerList'
            || $route.name === 'OrganizerDetail'
          "
          variant="text"
          class="font-weight-bold"
        >
          {{ $t('nav.organizers') }}
        </v-btn>
        <v-menu
          open-on-hover
          :open-delay="100"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              :active="
                $route.name === 'AlbumList'
                || $route.name === 'AlbumDetail'
                || $route.name === 'PhotoList'
                || $route.name === 'PhotoDetail'
              "
              variant="text"
              class="font-weight-bold"
              append-icon="mdi-chevron-down"
            >
              {{ $t('nav.photos') }}
            </v-btn>
          </template>
          <v-list density="compact">
            <v-list-item
              :to="{
                name: 'PhotoList',
                params: { locale: $i18n.locale },
                query: { tab: 'popular' }
              }"
              :active="
                ($route.name === 'PhotoList'
                  && $route.query.tab === 'popular')
                || ($route.name === 'PhotoDetail'
                  && $route.query.from === 'popular')
              "
            >
              {{ $t('nav.popular_photos') }}
            </v-list-item>
            <v-list-item
              :to="{
                name: 'PhotoList',
                params: { locale: $i18n.locale },
                query: { tab: 'fresh' }
              }"
              :active="
                ($route.name === 'PhotoList'
                  && $route.query.tab === 'fresh')
                || ($route.name === 'PhotoDetail'
                  && $route.query.from === 'fresh')
              "
            >
              {{ $t('nav.fresh_photos') }}
            </v-list-item>
            <v-list-item
              :to="{
                name: 'PhotoList',
                params: { locale: $i18n.locale },
                query: { tab: 'editors' }
              }"
              :active="
                ($route.name === 'PhotoList'
                  && $route.query.tab === 'editors')
                || ($route.name === 'PhotoDetail'
                  && $route.query.from === 'editors')
              "
            >
              {{ $t('nav.editors_choice') }}
            </v-list-item>
            <v-list-item
              :to="{
                name: 'AlbumList',
                params: { locale: $i18n.locale },
                query: { tab: 'popular' }
              }"
              :active="
                $route.name === 'AlbumList'
                || $route.name === 'AlbumDetail'
                || ($route.name === 'PhotoDetail'
                  && $route.query.from === 'album')
              "
            >
              {{ $t('nav.photo_albums') }}
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn
          :to="{
            name: 'Home',
            params: { locale: $i18n.locale }
          }"
          :active="$route.name === 'Home'"
          variant="text"
          class="font-weight-bold"
        >
          {{ $t('nav.awards') }}
        </v-btn>
        <v-btn
          :to="{
            name: 'ArticleList',
            params: { locale: $i18n.locale }
          }"
          :active="
            $route.name === 'ArticleList'
            || $route.name === 'ArticleDetail'
          "
          variant="text"
          class="font-weight-bold"
        >
          {{ $t('nav.blog') }}
        </v-btn>
      </nav>

      <div class="flex-grow-1">
        <div class="d-flex align-center justify-end">
          <HeaderSearch />
          <div
            v-if="userStore.isLoggedIn"
            class="d-flex align-center"
          >
            <HeaderNotifications />
            <HeaderUser />
          </div>
          <div
            v-else
            class="d-flex align-center ms-3"
          >
            <v-btn
              :to="{
                name: 'Login',
                params: { locale: $i18n.locale }
              }"
              variant="outlined"
              color="primary"
              rounded="xl"
              class="text-none"
            >
              {{ $t('auth.log_in') }}
            </v-btn>
            <v-btn
              :to="{
                name: 'Registration',
                params: { locale: $i18n.locale }
              }"
              variant="tonal"
              color="primary"
              rounded="xl"
              class="d-none d-lg-inline-flex text-none ms-1"
            >
              {{ $t('auth.register') }}
            </v-btn>
          </div>
        </div>
      </div>
    </v-container>
  </v-app-bar>

  <v-navigation-drawer
    v-model="navDrawer"
    location="start"
    temporary
  >
    <v-list
      density="compact"
      nav
    >
      <v-list-item
        :to="{
          name: 'OrganizerList',
          params: { locale: $i18n.locale }
        }"
        :active="$route.name === 'OrganizerList'"
        class="font-weight-bold text-uppercase"
      >
        {{ $t('nav.organizers') }}
      </v-list-item>
      <v-list-subheader
        class="font-weight-bold text-uppercase"
      >
        {{ $t('nav.photos') }}
      </v-list-subheader>
      <v-list-item
        :to="{
          name: 'PhotoList',
          params: { locale: $i18n.locale },
          query: { tab: 'popular' }
        }"
        :active="
          ($route.name === 'PhotoList'
            && $route.query.tab === 'popular')
          || ($route.name === 'PhotoDetail'
            && $route.query.from === 'popular')
        "
      >
        {{ $t('nav.popular_photos') }}
      </v-list-item>
      <v-list-item
        :to="{
          name: 'PhotoList',
          params: { locale: $i18n.locale },
          query: { tab: 'fresh' }
        }"
        :active="
          ($route.name === 'PhotoList'
            && $route.query.tab === 'fresh')
          || ($route.name === 'PhotoDetail'
            && $route.query.from === 'fresh')
        "
      >
        {{ $t('nav.fresh_photos') }}
      </v-list-item>
      <v-list-item
        :to="{
          name: 'PhotoList',
          params: { locale: $i18n.locale },
          query: { tab: 'editors' }
        }"
        :active="
          ($route.name === 'PhotoList'
            && $route.query.tab === 'editors')
          || ($route.name === 'PhotoDetail'
            && $route.query.from === 'editors')
        "
      >
        {{ $t('nav.editors_choice') }}
      </v-list-item>
      <v-list-item
        :to="{
          name: 'AlbumList',
          params: { locale: $i18n.locale },
          query: { tab: 'popular' }
        }"
        :active="
          $route.name === 'AlbumList'
          || $route.name === 'AlbumDetail'
          || ($route.name === 'PhotoDetail'
            && $route.query.from === 'album')
        "
      >
        {{ $t('nav.photo_albums') }}
      </v-list-item>
      <v-list-item
        :to="{
          name: 'Home',
          params: { locale: $i18n.locale }
        }"
        :active="$route.name === 'Home'"
        class="font-weight-bold text-uppercase"
      >
        {{ $t('nav.awards') }}
      </v-list-item>
      <v-list-item
        :to="{
          name: 'ArticleList',
          params: { locale: $i18n.locale }
        }"
        :active="
          $route.name === 'ArticleList'
          || $route.name === 'ArticleDetail'
        "
        class="font-weight-bold text-uppercase"
      >
        {{ $t('nav.blog') }}
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped>
a:hover {
  color: #e72a26 !important;
}
</style>
