// src/stores/post.js
import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase';
import { useAuthStore } from '@/modules/auth/stores/auth';

export const usePostStore = defineStore('post', {
  state: () => ({
    posts: [],
    loading: false,
    error: null,
    total: 0,
    currentPage: 1,
    itemsPerPage: 5,
    filters: {
      searchTerm: '',
      course: '',
      cycle: ''
    }
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

    async fetchPosts(options = {}) {
      // Evita múltiples llamadas simultáneas
      if (this.loading) return;
      
      this.loading = true;
      this.error = null;
      
      const {
        page = 1,
        reset = true,
        searchTerm = this.filters.searchTerm,
        course = this.filters.course,
        cycle = this.filters.cycle
      } = options;

      try {
        const offset = (page - 1) * this.itemsPerPage;
        const currentUserId = useAuthStore().user?.id || null;

        const { data, error } = await supabase.rpc('get_posts_with_ratings_paginated', {
          p_user_id: currentUserId,
          p_limit: this.itemsPerPage,
          p_offset: offset,
          p_search_term: searchTerm || null,
          p_course: course || null,
          p_cycle: cycle || null
        });

        if (error) throw error;

        if (reset) {
          // Solo resetea si se solicita explícitamente
          this.posts = data.posts || [];
        } else {
          // Para scroll infinito, concatena los resultados
          this.posts = [...this.posts, ...(data.posts || [])];
        }
        
        this.total = data.total || 0;
        this.currentPage = page;
        this.filters = { searchTerm, course, cycle };

        console.log('Posts loaded:', {
          posts: this.posts,
          total: this.total,
          filters: this.filters
        });

      } catch (err) {
        this.error = err.message;
        console.error('Error fetching posts:', err);
        this.posts = [];
        this.total = 0;
      } finally {
        this.loading = false;
      }
    },

    async applyFilters(filters = {}) {
      return this.fetchPosts({
        ...filters,
        reset: true
      });
    },

    async loadMorePosts() {
      if (this.posts.length >= this.total) return;
      return this.fetchPosts({
        page: this.currentPage + 1
      });
    },

    async clearFilters() {
      return this.applyFilters({
        searchTerm: '',
        course: '',
        cycle: ''
      });
    },

    async fetchAllCoursesByCycleData() {
      try {
        const { data, error } = await supabase
          .from('courses_by_cycle')
          .select('course_name, cycle_name'); // Seleccionamos ambas columnas

        if (error) throw error;
        this.allCoursesByCycleData = data || [];

        // Opcional: También poblar uniqueCourses y uniqueCycles si aún se necesitan listas completas
        const uniqueCoursesSet = new Set(data.map(item => item.course_name).filter(Boolean));
        const uniqueCyclesSet = new Set(data.map(item => item.cycle_name).filter(Boolean));
        this.courses = Array.from(uniqueCoursesSet).sort();
        this.cycles = Array.from(uniqueCyclesSet).sort();

      } catch (err) {
        console.error('Error fetching all courses by cycle data:', err.message);
        this.error = 'Error al cargar datos de cursos y ciclos.';
      }
    },


    async fetchUniqueCourses() {
      try {
        // Obtener valores distintos de la columna 'course_name' de la tabla 'courses_by_cycle'
        const { data, error } = await supabase
          .from('courses_by_cycle')
          .select('course_name', { distinct: true });

        if (error) throw error;
        // Mapea los resultados para obtener solo un array de strings y ordena
        this.courses = data.map(item => item.course_name).filter(Boolean).sort();
      } catch (err) {
        console.error('Error fetching unique courses from courses_by_cycle:', err.message);
        this.error = 'Error al cargar los cursos.';
      }
    },

    async fetchUniqueCycles() {
      try {
        // Forzar ciclos únicos del 1 al 10
        this.cycles = Array.from({ length: 10 }, (_, i) => `CICLO ${i + 1}`);
      } catch (err) {
        console.error('Error setting fixed cycles:', err.message);
        this.error = 'Error al cargar los ciclos.';
      }
    },

  async updatePost(postId, updateFields) {
  this.loading = true;
  this.error = null;
  
  try {
    const authStore = useAuthStore();
    const currentUserId = authStore.user?.id;

    // 1. Verificar que el post existe y pertenece al usuario
    const { data: existingPost, error: fetchError } = await supabase
      .from('posts')
      .select('id, user_id')
      .eq('id', postId)
      .single();

    if (fetchError || !existingPost) {
      throw new Error(fetchError?.message || 'La publicación no existe');
    }

    if (existingPost.user_id !== currentUserId) {
      throw new Error('No tienes permiso para editar esta publicación');
    }

    // 2. Actualización directa SIN esperar respuesta
    const { error: updateError } = await supabase
      .from('posts')
      .update(updateFields)
      .eq('id', postId);

    if (updateError) throw updateError;

    // 3. Actualizar el estado local MANUALMENTE
    const index = this.posts.findIndex(post => post.id === postId);
    if (index !== -1) {
      this.posts[index] = {
        ...this.posts[index],
        ...updateFields,
        updated_at: new Date().toISOString() // Agregar marca de tiempo
      };
    }

    // 4. Opcional: Recargar datos desde el servidor
    await this.fetchPosts();

    return this.posts[index];
    
  } catch (err) {
    this.error = err.message;
    console.error('Error en updatePost:', {
      error: err,
      postId,
      currentUser: authStore.user?.id,
      updateFields
    });
    throw err;
  } finally {
    this.loading = false;
  }
}

  }
});