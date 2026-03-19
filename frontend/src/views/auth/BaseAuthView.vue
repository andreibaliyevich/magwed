<template>
  <v-container
    fluid
    style="
      background-image: url('/bg.jpg');
      background-position: center;
      background-repeat: no-repeat;
      background-size: cover;
      min-height: 85vh;
    "
  >
    <v-row
      align="center"
      justify="center"
      style="min-height: 85vh;"
    >
      <v-col
        xs="12"
        sm="8"
        md="6"
        lg="4"
      >
        <v-sheet
          :elevation="3"
          color="white"
          rounded="lg"
          class="pa-10"
        >
          <router-view />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>
