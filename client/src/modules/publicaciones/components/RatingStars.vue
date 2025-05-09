<template>
  <div>
    <v-icon
      v-for="n in 5"
      :key="n"
      :color="n <= hover || n <= valor ? 'blue' : 'grey lighten-1'"
      @click="emit('rate', n)"
      @mouseover="hover = n"
      @mouseleave="hover = 0"
      small
    >mdi-star</v-icon>
  </div>
</template>

<script setup>
import { ref } from 'vue';
defineProps(['valor']);
const emit = defineEmits(['rate']);
const hover = ref(0);
</script>