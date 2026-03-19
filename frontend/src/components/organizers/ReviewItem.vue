<script setup>
import { useUserStore } from '@/stores/user.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'
import ReportListItemDialog from '../ReportListItemDialog.vue'

const userStore = useUserStore()

const props = defineProps({
  reviewItem: {
    type: Object,
    required: true
  }
})

const { getLocaleDateTimeString } = useLocaleDateTime()
</script>

<template>
  <div class="d-flex ga-3">
    <router-link
      v-if="reviewItem.author.profile_url"
      :to="{
        name: 'OrganizerDetail',
        params: { profile_url: reviewItem.author.profile_url }
      }"
    >
      <AvatarExtended
        :image="reviewItem.author.avatar"
        :size="48"
        :online="reviewItem.author.status === 'online' ? true : false"
      />
    </router-link>
    <AvatarExtended
      v-else
      :image="reviewItem.author.avatar"
      :size="48"
      :online="reviewItem.author.status === 'online' ? true : false"
    />

    <div class="flex-grow-1">
      <div class="d-flex justify-space-between">
        <router-link
          v-if="reviewItem.author.profile_url"
          :to="{
            name: 'OrganizerDetail',
            params: { profile_url: reviewItem.author.profile_url }
          }"
          class="text-decoration-none text-black"
        >
          <strong>{{ reviewItem.author.name }}</strong>
        </router-link>
        <strong v-else>
          {{ reviewItem.author.name }}
        </strong>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(reviewItem.created_at) }}
        </small>
      </div>

      <div class="d-flex justify-space-between">
        <v-rating
          :model-value="reviewItem.rating"
          readonly
          :length="5"
          density="compact"
          size="small"
          color="orange-lighten-1"
        ></v-rating>

        <v-menu
          v-if="userStore.isLoggedIn"
          location="start"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              icon="mdi-dots-horizontal"
              variant="text"
              size="small"
            ></v-btn>
          </template>
          <template v-slot:default="{ isActive }">
            <v-list density="compact">
              <ReportListItemDialog
                contentType="review"
                :objectUUID="reviewItem.uuid"
                @reportSent="isActive.value = false"
              />
            </v-list>
          </template>
        </v-menu>
      </div>
      <div style="white-space: pre-line;">
        {{ reviewItem.comment }}
      </div>
    </div>
  </div>
</template>
