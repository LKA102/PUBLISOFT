
<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Notificaciones</h2>
    <ul>
      <li v-for="note in notifications" :key="note.id" class="mb-2">
        {{ note.message }} - {{ new Date(note.created_at).toLocaleString() }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { supabase } from '@/services/supabase'

const notifications = ref([])

onMounted(async () => {
  const user = (await supabase.auth.getUser()).data.user
  const { data } = await supabase.from('notifications').select('*').eq('user_id', user.id).order('created_at', { ascending: false }).limit(10)
  notifications.value = data
})
</script>
