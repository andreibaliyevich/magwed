<template>
  <div class="text-center">
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'design',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'design'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.design') }}
    </v-btn>
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'fashion',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'fashion'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.fashion') }}
    </v-btn>
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'inspiration',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'inspiration'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.inspiration') }}
    </v-btn>
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'journey',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'journey'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.journey') }}
    </v-btn>
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'lifestyle',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'lifestyle'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.lifestyle') }}
    </v-btn>
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'photography',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'photography'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.photography') }}
    </v-btn>
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'technology',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'technology'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.technology') }}
    </v-btn>
    <v-btn
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: 'wedding',
          year: $route.query.year
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.category === 'wedding'
      "
      variant="text"
      class="text-none"
    >
      {{ $t('category_choices.wedding') }}
    </v-btn>
  </div>
</template>