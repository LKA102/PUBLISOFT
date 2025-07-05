// src/stores/post.js
import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase';
import { useAuthStore } from './auth'; // Necesitamos el usuario actual

export const usePostStore = defineStore('post', {
  state: () => ({
    posts: [],
    loading: false,
    error: null,
    total: 0, // Nuevo: total de publicaciones
  }),

  actions: {
    async uploadPost(postData, file) {
      this.loading = true;
      this.error = null;
      const authStore = useAuthStore();

      if (!authStore.user) {
        this.error = 'Debes iniciar sesión para publicar.';
        this.loading = false;
        alert(this.error);
        return;
      }

      const userId = authStore.user.id;
      const bucketName = 'publications'; // ¡Asegúrate que este sea el nombre de tu bucket!

      try {
        // 1. Subir el archivo a Supabase Storage
        const fileExtension = file.name.split('.').pop();
        const fileName = `${Date.now()}-${Math.random().toString(36).substring(2, 9)}.${fileExtension}`;
        const filePath = `${userId}/${fileName}`;

        console.log(`Subiendo archivo a: ${bucketName}/${filePath}`);
        const { data: uploadData, error: uploadError } = await supabase.storage
          .from(bucketName)
          .upload(filePath, file);

        if (uploadError) {
          throw new Error(`Error al subir el archivo: ${uploadError.message}`);
        }
        console.log('Archivo subido con éxito:', uploadData);

        const { data: publicUrlData } = supabase.storage
          .from(bucketName)
          .getPublicUrl(filePath);
        
        const fileUrl = publicUrlData.publicUrl;
        console.log('--- URL GENERADA PARA EL ARCHIVO ---:', fileUrl);

        // 2. Insertar la publicación en la tabla 'posts'
        console.log('Insertando publicación en la base de datos...');
        const { data: postResult, error: postError } = await supabase
          .from('posts')
          .insert({
            user_id: userId,
            title: postData.title,
            course: postData.course,
            cycle: postData.cycle,
            file_url: fileUrl,
            file_type: fileExtension,
          })
          .select(`
            *,
            users (
              email,
              alias,
              role,
              avatar_url
            )
          `)
          .single();

        if (postError) {
          throw new Error(`Error al insertar la publicación en la DB: ${postError.message}`);
        }
        console.log('Publicación insertada con éxito:', postResult);

        // Después de subir un post, recargamos todas las publicaciones para incluir los promedios actualizados
        // y asegurar que el nuevo post tenga los campos de rating.
        await this.fetchPosts(); 
        
        alert('¡Publicación creada con éxito!');
        return postResult;

      } catch (err) {
        this.error = err.message;
        console.error('Error al subir la publicación:', err.message);
        alert(`Error al subir la publicación: ${err.message}`);
      } finally {
        this.loading = false;
      }
    },

    async fetchPosts(page = 1, limit = 5) {
      this.loading = true;
      this.error = null;
      const authStore = useAuthStore();
      const currentUserId = authStore.user?.id || null;

      const offset = (page - 1) * limit;

      try {
        const { data, error } = await supabase
          .rpc('get_posts_with_ratings_paginated', {
            p_user_id: currentUserId,
            p_limit: limit,
            p_offset: offset
          });

        if (error) throw error;

        this.posts = data.posts;
        this.total = data.total;
        console.log(`Cargadas ${this.posts.length} de ${this.total} publicaciones`);
      } catch (err) {
        this.error = err.message;
        console.error('Error al cargar publicaciones:', err.message);
      } finally {
        this.loading = false;
      }
    }

  }
});