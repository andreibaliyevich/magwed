<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { useCurrencyStore } from '@/stores/currency.js'
import { useLocaleDateTime } from '@/composables/localeDateTime.js'

const currencyStore = useCurrencyStore()

const searchLoading = ref(false)
const searchQuery = ref('')
const searchType = ref('organizers')
const searchedItems = ref([])
const nextURL = ref(null)

const { getLocaleDateString } = useLocaleDateTime()

const openCloseDialog = (value) => {
  if (!value) {
    searchQuery.value = ''
    searchedItems.value = []
    nextURL.value = null
  }
}

const searchItems = async () => {
  searchLoading.value = true

  let requestUrl = ''
  if (searchType.value === 'organizers') {
    requestUrl = '/accounts/organizers/'
  } else if (searchType.value === 'photos') {
    requestUrl = '/portfolio/photo/list/'
  } else if (searchType.value === 'albums') {
    requestUrl = '/portfolio/album/list/'
  } else if (searchType.value === 'articles') {
    requestUrl = '/blog/article/list/'
  }

  try {
    const response = await axios.get(requestUrl, {
      params: {
        search: searchQuery.value
      }
    })
    searchedItems.value = response.data.results
    nextURL.value = response.data.next
  } catch (error) {
    console.error(error)
  } finally {
    searchLoading.value = false
  }
}

const getMoreItems = async ({ done }) => {
  if (nextURL.value) {
    try {
      const response = await axios.get(nextURL.value)
      searchedItems.value = [...searchedItems.value, ...response.data.results]
      nextURL.value = response.data.next
      done('ok')
    } catch (error) {
      console.error(error)
      done('error')
    }
  } else {
    done('empty')
  }
}

watch(searchQuery, async (newValue) => {
  if (newValue) {
    await searchItems()
  } else {
    searchedItems.value = []
  }
})

watch(searchType, async () => {
  if (searchQuery.value) {
    searchedItems.value = []
    await searchItems()
  }
})
</script>

<template>
  <v-dialog
    @update:modelValue="openCloseDialog"
    :width="600"
    class="mt-12"
  >
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        icon="mdi-magnify"
      ></v-btn>
    </template>
    <template v-slot:default="{ isActive }">
      <v-card rounded="lg">
        <v-text-field
          v-model="searchQuery"
          :loading="searchLoading"
          type="search"
          autofocus
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          enterkeyhint="search"
          spellcheck="false"
          clearable
          variant="filled"
          prepend-inner-icon="mdi-magnify"
          :placeholder="$t('search.search2')"
        ></v-text-field>

        <div class="d-flex justify-center mb-5">
          <v-btn-toggle
            v-model="searchType"
            density="compact"
            mandatory
          >
            <v-btn value="organizers">
              {{ $t('organizers.organizers') }}
            </v-btn>
            <v-btn value="photos">
              {{ $t('portfolio.photos') }}
            </v-btn>
            <v-btn value="albums">
              {{ $t('portfolio.photo_albums') }}
            </v-btn>
            <v-btn value="articles">
              {{ $t('blog.articles') }}
            </v-btn>
          </v-btn-toggle>
        </div>

        <v-infinite-scroll
          v-if="searchedItems.length > 0"
          @load="getMoreItems"
          mode="intersect"
          :empty-text="$t('search.no_more_results')"
        >
          <template v-if="searchType === 'organizers'">
            <div
              v-for="organizer in searchedItems"
              :key="organizer.user.uuid"
              class="mx-1 my-1"
            >
              <v-card rounded="lg">
                <template v-slot:prepend>
                  <router-link
                    :to="{
                      name: 'OrganizerDetail',
                      params: {
                        locale: $i18n.locale,
                        profile_url: organizer.user.profile_url
                      }
                    }"
                    @click="isActive.value = false"
                  >
                    <AvatarExtended
                      :image="organizer.user.avatar"
                      :size="64"
                      :online="organizer.user.status === 'online' ? true : false"
                    />
                  </router-link>
                </template>
                <template v-slot:title>
                  <router-link
                    :to="{
                      name: 'OrganizerDetail',
                      params: {
                        locale: $i18n.locale,
                        profile_url: organizer.user.profile_url
                      }
                    }"
                    @click="isActive.value = false"
                    class="text-black text-decoration-none"
                  >
                    {{ organizer.user.name }}
                  </router-link>
                </template>
                <template v-slot:subtitle>
                  <p v-if="organizer.cost_work">
                    {{ currencyStore.currencySymbol }}{{ currencyStore.convertCurrency(organizer.cost_work) }}
                    {{ $t('organizers.per_hour') }}
                    <small
                      v-if="organizer.number_hours"
                      class="text-secondary"
                    >
                      {{ $t('organizers.min_number_hours', { n: organizer.number_hours }) }}
                    </small>
                  </p>
                </template>
              </v-card>
            </div>
          </template>
          <template v-else-if="searchType === 'photos'">
            <div
              v-for="photo in searchedItems"
              :key="photo.uuid"
              class="mx-1 my-1"
            >
              <v-card rounded="lg">
                <v-row class="me-3">
                  <v-col
                    :cols="12"
                    :sm="4"
                  >
                    <router-link
                      :to="{
                        name: 'PhotoDetail',
                        params: {
                          locale: $i18n.locale,
                          uuid: photo.uuid
                        }
                      }"
                      @click="isActive.value = false"
                    >
                      <v-img
                        :src="photo.thumbnail"
                        aspect-ratio="1/1"
                        cover
                      ></v-img>
                    </router-link>
                  </v-col>
                  <v-col
                    :cols="12"
                    :sm="8"
                    class="my-3"
                  >
                    <div class="d-flex flex-column h-100">
                      <router-link
                        v-if="photo.title"
                        :to="{
                          name: 'PhotoDetail',
                          params: {
                            locale: $i18n.locale,
                            uuid: photo.uuid
                          }
                        }"
                        @click="isActive.value = false"
                        class="text-black text-decoration-none"
                      >
                        <h5 class="text-h5">{{ photo.title }}</h5>
                      </router-link>
                      <div class="d-flex align-center mt-auto">
                        <router-link
                          :to="{
                            name: 'OrganizerDetail',
                            params: {
                              locale: $i18n.locale,
                              profile_url: photo.author.profile_url
                            }
                          }"
                          @click="isActive.value = false"
                        >
                          <v-avatar :size="32">
                            <v-img
                              v-if="photo.author.avatar"
                              :src="photo.author.avatar"
                              :alt="photo.author.name"
                            ></v-img>
                            <v-icon
                              v-else
                              icon="mdi-account-circle"
                              :size="32"
                            ></v-icon>
                          </v-avatar>
                        </router-link>
                        <router-link
                          :to="{
                            name: 'OrganizerDetail',
                            params: {
                              locale: $i18n.locale,
                              profile_url: photo.author.profile_url
                            }
                          }"
                          @click="isActive.value = false"
                          class="text-black text-decoration-none ms-2"
                        >
                          {{ photo.author.name }}
                        </router-link>
                      </div>
                      <div class="d-flex justify-space-between mt-auto">
                        <div class="text-grey-darken-2">
                          <v-icon
                            icon="mdi-eye-outline"
                            size="default"
                          ></v-icon>
                          {{ photo.view_count }}
                        </div>
                        <div class="text-grey-darken-2">
                          <v-icon
                            icon="mdi-heart-outline"
                            size="default"
                          ></v-icon>
                          {{ photo.like_count }}
                        </div>
                        <div class="text-grey-darken-2">
                          <v-icon
                            icon="mdi-star-outline"
                            size="default"
                          ></v-icon>
                          {{ photo.rating }}
                        </div>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-card>
            </div>
          </template>
          <template v-else-if="searchType === 'albums'">
            <div
              v-for="album in searchedItems"
              :key="album.uuid"
              class="mx-1 my-1"
            >
              <v-card rounded="lg">
                <v-row class="me-3">
                  <v-col
                    :cols="12"
                    :sm="4"
                  >
                    <router-link
                      :to="{
                        name: 'AlbumDetail',
                        params: {
                          locale: $i18n.locale,
                          uuid: album.uuid
                        }
                      }"
                      @click="isActive.value = false"
                    >
                      <v-img
                        :src="album.thumbnail"
                        aspect-ratio="1/1"
                        cover
                      ></v-img>
                    </router-link>
                  </v-col>
                  <v-col
                    :cols="12"
                    :sm="8"
                    class="my-3"
                  >
                    <div class="d-flex flex-column h-100">
                      <router-link
                        v-if="album.title"
                        :to="{
                          name: 'AlbumDetail',
                          params: {
                            locale: $i18n.locale,
                            uuid: album.uuid
                          }
                        }"
                        @click="isActive.value = false"
                        class="text-black text-decoration-none"
                      >
                        <h5 class="text-h5">{{ album.title }}</h5>
                      </router-link>
                      <div class="d-flex align-center mt-auto">
                        <router-link
                          :to="{
                            name: 'OrganizerDetail',
                            params: {
                              locale: $i18n.locale,
                              profile_url: album.author.profile_url
                            }
                          }"
                          @click="isActive.value = false"
                        >
                          <v-avatar :size="32">
                            <v-img
                              v-if="album.author.avatar"
                              :src="album.author.avatar"
                              :alt="album.author.name"
                            ></v-img>
                            <v-icon
                              v-else
                              icon="mdi-account-circle"
                              :size="32"
                            ></v-icon>
                          </v-avatar>
                        </router-link>
                        <router-link
                          :to="{
                            name: 'OrganizerDetail',
                            params: {
                              locale: $i18n.locale,
                              profile_url: album.author.profile_url
                            }
                          }"
                          @click="isActive.value = false"
                          class="text-black text-decoration-none ms-2"
                        >
                          {{ album.author.name }}
                        </router-link>
                      </div>
                      <div class="d-flex justify-space-between mt-auto">
                        <div class="text-grey-darken-2">
                          <v-icon
                            icon="mdi-eye-outline"
                            size="default"
                          ></v-icon>
                          {{ album.view_count }}
                        </div>
                        <div class="text-grey-darken-2">
                          <v-icon
                            icon="mdi-heart-outline"
                            size="default"
                          ></v-icon>
                          {{ album.like_count }}
                        </div>
                        <div class="text-grey-darken-2">
                          <v-icon
                            icon="mdi-star-outline"
                            size="default"
                          ></v-icon>
                          {{ album.rating }}
                        </div>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-card>
            </div>
          </template>
          <template v-else-if="searchType === 'articles'">
            <div
              v-for="article in searchedItems"
              :key="article.slug"
              class="mx-1 my-1"
            >
              <v-card rounded="lg">
                <router-link
                  :to="{
                    name: 'ArticleDetail',
                    params: {
                      locale: $i18n.locale,
                      slug: article.slug
                    }
                  }"
                  @click="isActive.value = false"
                  class="text-black text-decoration-none"
                >
                  <v-img
                    :src="article.thumbnail"
                    :height="200"
                    cover
                    class="align-end text-white"
                  >
                    <v-card-title>{{ article.translated_title }}</v-card-title>
                  </v-img>
                </router-link>
                <v-card-subtitle>
                  <div class="d-flex flex-wrap ga-1 py-2">
                    <v-chip
                      v-for="categoryValue in article.categories"
                      :key="`${article.slug}-category-${categoryValue}`"
                      density="compact"
                    >
                      {{ $t(`category_choices.${categoryValue}`) }}
                    </v-chip>
                  </div>
                  <v-icon
                    icon="mdi-calendar-month-outline"
                    size="default"
                  ></v-icon>
                  {{ getLocaleDateString(article.published_at) }}
                </v-card-subtitle>
                <v-card-text>
                  {{ article.translated_description }}
                </v-card-text>
              </v-card>
            </div>
          </template>
        </v-infinite-scroll>
        <div
          v-else-if="searchQuery && !searchLoading"
          class="text-center"
        >
          <v-icon
            icon="mdi-feature-search-outline"
            :size="150"
            color="secondary"
          ></v-icon>
          <p class="mt-8">{{ $t('search.no_results_found') }}</p>
        </div>
        <div
          v-else
          class="text-center"
        >
          <v-icon
            icon="mdi-text-box-search-outline"
            :size="150"
            color="secondary"
          ></v-icon>
          <p class="mt-8">{{ $t('search.results_will_here') }}</p>
        </div>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="isActive.value = false">{{ $t('btn.close') }}</v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 0.3em;
}
@media (max-width: 600px) {
  .v-btn-toggle > button {
    font-size: 0.75rem;
    min-width: 50px;
    padding: 0 12px;
  }
}
</style>
