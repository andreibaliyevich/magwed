<script setup>
import { messageType, reasonOfNotification } from '@/config.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

defineProps({
  notice: {
    type: Object,
    required: true
  }
})
const { getLocaleDateTimeString } = useLocaleDateTime()
</script>

<template>
  <div
    class="d-flex ma-1"
    :data-uuid="notice.uuid"
  >

    <router-link
      v-if="notice.initiator.profile_url"
      :to="{
        name: 'OrganizerDetail',
        params: {
          locale: $i18n.locale,
          profile_url: notice.initiator.profile_url
        }
      }"
    >
      <v-avatar size="small">
        <v-img
          v-if="notice.initiator.avatar"
          :src="notice.initiator.avatar"
          :alt="notice.initiator.name"
        ></v-img>
        <v-icon
          v-else
          icon="mdi-account-circle"
          size="x-large"
        ></v-icon>
      </v-avatar>
    </router-link>
    <v-avatar
      v-else
      size="small"
    >
      <v-img
        v-if="notice.initiator.avatar"
        :src="notice.initiator.avatar"
        :alt="notice.initiator.name"
      ></v-img>
      <v-icon
        v-else
        icon="mdi-account-circle"
        size="x-large"
      ></v-icon>
    </v-avatar>

    <div
      v-if="notice.reason === reasonOfNotification.FOLLOW"
      class="d-flex flex-wrap ms-2"
    >
      <p>
        {{ $t('notifications.follow', { user_name: notice.initiator.name }) }}
      </p>
      <small class="text-secondary">
        {{ getLocaleDateTimeString(notice.created_at) }}
      </small>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.ARTICLE"
      class="d-flex justify-space-between align-center w-100 ms-2"
    >
      <div class="d-flex align-content-space-between flex-wrap h-100">
        <p>
          {{
            $t('notifications.article', { user_name: notice.initiator.name })
          }}
        </p>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <router-link
        :to="{
          name: 'ArticleDetail',
          params: {
            locale: $i18n.locale,
            slug: notice.content_object.slug
          }
        }"
      >
        <v-img
          :src="notice.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.ALBUM"
      class="d-flex justify-space-between align-center w-100 ms-2"
    >
      <div class="d-flex align-content-space-between flex-wrap h-100">
        <p>
          {{
            $t('notifications.album', {
              user_name: notice.initiator.name,
              album_title: notice.content_object.title
            })
          }}
        </p>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <router-link
        :to="{
          name: 'AlbumDetail',
          params: {
            locale: $i18n.locale,
            uuid: notice.content_object.uuid
          }
        }"
      >
        <v-img
          :src="notice.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.PHOTO"
      class="d-flex justify-space-between align-center w-100 ms-2"
    >
      <div class="d-flex align-content-space-between flex-wrap h-100">
        <p v-if="notice.content_object.title">
          {{
            $t('notifications.photo_title', {
              user_name: notice.initiator.name,
              photo_title: notice.content_object.title
            })
          }}
        </p>
        <p v-else>
          {{ $t('notifications.photo', { user_name: notice.initiator.name }) }}
        </p>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <router-link
        :to="{
          name: 'PhotoDetail',
          params: {
            locale: $i18n.locale,
            uuid: notice.content_object.uuid
          }
        }"
      >
        <v-img
          :src="notice.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.LIKE_ALBUM"
      class="d-flex justify-space-between align-center w-100 ms-2"
    >
      <div class="d-flex align-content-space-between flex-wrap h-100">
        <p>
          {{
            $t('notifications.like_album', {
              user_name: notice.initiator.name,
              album_title: notice.content_object.title
            })
          }}
        </p>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <router-link
        :to="{
          name: 'AlbumDetail',
          params: {
            locale: $i18n.locale,
            uuid: notice.content_object.uuid
          }
        }"
      >
        <v-img
          :src="notice.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.LIKE_PHOTO"
      class="d-flex justify-space-between align-center w-100 ms-2"
    >
      <div class="d-flex align-content-space-between flex-wrap h-100">
        <p v-if="notice.content_object.title">
          {{
            $t('notifications.like_photo_title', {
              user_name: notice.initiator.name,
              photo_title: notice.content_object.title
            })
          }}
        </p>
        <p v-else>
          {{
            $t('notifications.like_photo', { user_name: notice.initiator.name })
          }}
        </p>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <router-link
        :to="{
          name: 'PhotoDetail',
          params: {
            locale: $i18n.locale,
            uuid: notice.content_object.uuid
          }
        }"
      >
        <v-img
          :src="notice.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.COMMENT"
      class="d-flex justify-space-between align-center w-100 ms-2"
    >
      <div class="d-flex align-content-space-between flex-wrap h-100">
        <p v-if="notice.content_object.content_type_model === 'article'">
          {{
            $t('notifications.comment_article', {
              user_name: notice.initiator.name,
              content: notice.content_object.content
            })
          }}
        </p>
        <p v-else-if="notice.content_object.content_type_model === 'album'">
          {{
            $t('notifications.comment_album', {
              user_name: notice.initiator.name,
              content: notice.content_object.content,
              album_title: notice.content_object.content_object.title
            })
          }}
        </p>
        <p v-else-if="notice.content_object.content_type_model === 'photo'">
          <div v-if="notice.content_object.content_object.title">
            {{
              $t('notifications.comment_photo_title', {
                user_name: notice.initiator.name,
                content: notice.content_object.content,
                photo_title: notice.content_object.content_object.title
              })
            }}
          </div>
          <div v-else>
            {{
              $t('notifications.comment_photo', {
                user_name: notice.initiator.name,
                content: notice.content_object.content
              })
            }}
          </div>
        </p>
        <p v-else-if="notice.content_object.content_type_model === 'comment'">
          <div v-if="notice.content_object.content_object.model_name === 'article'">
            {{
              $t('notifications.comment_comment_article', {
                user_name: notice.initiator.name,
                content: notice.content_object.content
              })
            }}
          </div>
          <div v-else-if="notice.content_object.content_object.model_name === 'album'">
            {{
              $t('notifications.comment_comment_album', {
                user_name: notice.initiator.name,
                content: notice.content_object.content,
                album_title: notice.content_object.content_object.title
              })
            }}
          </div>
          <div v-else-if="notice.content_object.content_object.model_name === 'photo'">
            <div v-if="notice.content_object.content_object.title">
              {{
                $t('notifications.comment_comment_photo_title', {
                  user_name: notice.initiator.name,
                  content: notice.content_object.content,
                  photo_title: notice.content_object.content_object.title
                })
              }}
            </div>
            <div v-else>
              {{
                $t('notifications.comment_comment_photo', {
                  user_name: notice.initiator.name,
                  content: notice.content_object.content
                })
              }}
            </div>
          </div>
        </p>
        <small class="text-secondary">
          {{ getLocaleDateTimeString(notice.created_at) }}
        </small>
      </div>
      <router-link
        v-if="notice.content_object.content_object.model_name === 'article'"
        :to="{
          name: 'ArticleDetail',
          params: {
            locale: $i18n.locale,
            slug: notice.content_object.content_object.slug
          }
        }"
      >
        <v-img
          :src="notice.content_object.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
      <router-link
        v-else-if="notice.content_object.content_object.model_name === 'album'"
        :to="{
          name: 'AlbumDetail',
          params: {
            locale: $i18n.locale,
            uuid: notice.content_object.content_object.uuid
          }
        }"
      >
        <v-img
          :src="notice.content_object.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
      <router-link
        v-else-if="notice.content_object.content_object.model_name === 'photo'"
        :to="{
          name: 'PhotoDetail',
          params: {
            locale: $i18n.locale,
            uuid: notice.content_object.content_object.uuid
          }
        }"
      >
        <v-img
          :src="notice.content_object.content_object.thumbnail"
          :width="64"
          :aspect-ratio="1/1"
          cover
        ></v-img>
      </router-link>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.REVIEW"
      class="d-flex flex-wrap ms-2"
    >
      <p>
        {{ $t('notifications.review', { user_name: notice.initiator.name }) }}
        ({{ $t('reviews.rating_options', { n: notice.content_object.rating }) }}):
        {{ notice.content_object.comment }}
      </p>
      <small class="text-secondary">
        {{ getLocaleDateTimeString(notice.created_at) }}
      </small>
    </div>

    <div
      v-else-if="notice.reason === reasonOfNotification.MESSAGE"
      class="d-flex flex-wrap ms-2"
    >
      <router-link
        :to="{
          name: 'Chat',
          params: {
            locale: $i18n.locale,
            uuid: notice.content_object.chat
          }
        }"
        class="text-decoration-none text-black"
      >
        <p v-if="notice.content_object.msg_type === messageType.TEXT">
          {{ $t('notifications.message', { user_name: notice.initiator.name }) }}:
          {{ notice.content_object.content }}
        </p>
        <p v-else-if="notice.content_object.msg_type === messageType.IMAGES">
          {{ $t('notifications.message', { user_name: notice.initiator.name }) }}:
          {{ $t('messenger.images', { n: notice.content_object.content }) }}
        </p>
        <p v-else-if="notice.content_object.msg_type === messageType.FILES">
          {{ $t('notifications.message', { user_name: notice.initiator.name }) }}:
          {{ $t('messenger.files', { n: notice.content_object.content }) }}
        </p>
      </router-link>
      <small class="text-secondary">
        {{ getLocaleDateTimeString(notice.created_at) }}
      </small>
    </div>

  </div>
</template>
