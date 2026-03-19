<script setup>
import { ref } from 'vue'
import CategoriesFilter from '@/components/blog/CategoriesFilter.vue'
import YearsFilter from '@/components/blog/YearsFilter.vue'

const blogFiltersDrawer = ref(false)
</script>

<template>
  <v-container>
    <v-btn
      @click.stop="blogFiltersDrawer = !blogFiltersDrawer"
      variant="outlined"
      block
      class="d-inline-flex d-md-none"
      append-icon="mdi-filter-outline"
    >
      {{ $t('blog.filters') }}
    </v-btn>
    <v-navigation-drawer
      v-model="blogFiltersDrawer"
      location="end"
      temporary
    >
      <h6 class="text-h6 text-center mt-3">
        {{ $t('blog.categories') }}
      </h6>
      <CategoriesFilter />

      <v-divider class="my-5"></v-divider>

      <h6 class="text-h6 text-center mt-3">
        {{ $t('blog.years') }}
      </h6>
      <YearsFilter />
    </v-navigation-drawer>

    <v-row>
      <v-col
        :cols="12"
        :md="8"
      >
        <router-view />
      </v-col>
      <v-col
        :cols="12"
        :md="4"
      >
        <v-sheet
          :elevation="1"
          rounded="lg"
          class="d-none d-md-block position-sticky mt-5 pa-3"
        >
          <h6 class="text-h6">
            {{ $t('blog.categories') }}
          </h6>
          <CategoriesFilter />

          <v-divider class="my-5"></v-divider>

          <h6 class="text-h6">
            {{ $t('blog.years') }}
          </h6>
          <YearsFilter />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.d-none.d-md-block.position-sticky {
  top: 82px;
}
</style>
