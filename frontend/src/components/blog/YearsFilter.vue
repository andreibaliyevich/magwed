<script setup>
const getYears = () => {
  let result = []
  let currentYear = new Date().getFullYear()
  for (let i = 2022; i <= currentYear; i++) {
    result.push(i)
  }
  return result
}
</script>

<template>
  <div class="text-center">
    <v-btn
      v-for="yearNumber in getYears()"
      :to="{
        name: 'ArticleList',
        query: {
          author: $route.query.author,
          category: $route.query.category,
          year: yearNumber
        }
      }"
      :active="
        $route.name === 'ArticleList'
          && $route.query.year == yearNumber
      "
      variant="text"
      class="text-none"
    >
      {{ yearNumber }}
    </v-btn>
  </div>
</template>