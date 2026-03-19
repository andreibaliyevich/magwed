<script setup>
import axios from 'axios'

const props = defineProps({
  objFavorite: {
    type: Boolean,
    required: true
  },
  contentType: {
    type: String,
    required: true
  },
  objectUUID: {
    type: String,
    required: true
  }
})
const emit = defineEmits(['favoriteUpdated'])

const addToFavorites = async () => {
  try {
    const response = await axios.post('/social/favorite/', {
      content_type: props.contentType,
      object_uuid: props.objectUUID
    })
    if (response.status === 201) {
      emit('favoriteUpdated', true)
    }
  } catch (error) {
    console.error(error)
  }
}

const removeFromFavorites = async () => {
  try {
    const response = await axios.delete('/social/favorite/', {
      data: {
        content_type: props.contentType,
        object_uuid: props.objectUUID
      }
    })
    if (response.status === 204) {
      emit('favoriteUpdated', false)
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <v-list-item
    v-if="objFavorite"
    @click="removeFromFavorites()"
    prepend-icon="mdi-star"
  >
    {{ $t('favorites.remove_from_favourites') }}
  </v-list-item>
  <v-list-item
    v-else
    @click="addToFavorites()"
    prepend-icon="mdi-star-outline"
  >
    {{ $t('favorites.add_to_favourites') }}
  </v-list-item>
</template>
