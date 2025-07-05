
<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Mis Publicaciones</h2>
    <div v-for="post in myPosts" :key="post.id" class="border p-4 mb-4">
      <h3 class="font-semibold">{{ post.title }}</h3>
      <button class="bg-red-500 text-white px-2 py-1 text-sm" @click="deletePost(post.id)">Eliminar</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { supabase } from '@/services/supabase'

const myPosts = ref([])

onMounted(async () => {
  const user = (await supabase.auth.getUser()).data.user
  const { data } = await supabase.from('posts').select('*').eq('user_id', user.id)
  myPosts.value = data
})

async function deletePost(id) {
  const confirmDelete = confirm('¿Estás seguro de que deseas eliminar esta publicación?');
  if (!confirmDelete) return;

  const { error } = await supabase.from('posts').delete().eq('id', id);

  if (error) {
    alert('Error al eliminar: ' + error.message);
    console.error('Error al eliminar:', error);
    return;
  }

  // Si no hay error, eliminamos de la lista local
  myPosts.value = myPosts.value.filter(p => p.id !== id);
}
</script>
