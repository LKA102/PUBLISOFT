<template>
  <div>
    <v-icon
      v-for="n in 5"
      :key="n"
      :color="n <= hover || n <= valor ? 'yellow' : 'grey'"
      @click="emit('rate', n)"
      @mouseover="hover = n"
      @mouseleave="hover = 0"
    >mdi-star</v-icon>
  </div>
</template>

<script setup>
import { ref } from 'vue';
defineProps(['valor']);
const emit = defineEmits(['rate']);
const hover = ref(0);
</script>
