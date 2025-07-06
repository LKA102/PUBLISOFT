// src/stores/post.js
import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase';
import { useAuthStore } from '@modules/auth/stores/auth'; // Necesitamos el usuario actual

export const usePostStore = defineStore('post', {
  state: () => ({
    posts: [],
    loading: false,
    error: null,
    allCoursesByCycleData: [],
    courses: [], // Nuevo estado para almacenar cursos únicos
    cycles: [],  // Nuevo estado para almacenar ciclos únicos
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

    async fetchPosts(filters = {}) {
      this.loading = true;
      this.error = null;
      // Obtener el ID del usuario actual para saber su calificación
      const authStore = useAuthStore();
      const currentUserId = authStore.user?.id;

      try {
        let query = supabase
          .from('posts')
          .select(`
            *,
            users (alias, email, avatar_url, role),
            ratings (rating, user_id)
          `);

        // Aplicar filtro de búsqueda por texto
        if (filters.searchTerm) {
          const searchTerm = `%${filters.searchTerm.toLowerCase()}%`;
          query = query.or(`title.ilike.${searchTerm},course.ilike.${searchTerm},cycle.ilike.${searchTerm}`);
        }

        // Aplicar filtro por curso
        if (filters.course) {
          query = query.eq('course', filters.course);
        }

        // Aplicar filtro por ciclo
        if (filters.cycle) {
          query = query.eq('cycle', filters.cycle);
        }

             // **********************************************
        // *** NUEVA LÓGICA CLAVE: Filtrar por rol del autor ***
        // **********************************************
        if (filters.authorRole) {
          // Si queremos filtrar por 'role' de la tabla 'users' que está unida.
          // Supabase's `select` con joins como `users(role)` permite filtrar,
          // pero el `.eq` directo sobre la columna anidada es más reciente o requiere sintaxis específica.
          // La forma más robusta es obtener los IDs de los usuarios con ese rol primero y luego filtrar por `user_id`.
          
          const { data: usersWithRole, error: usersError } = await supabase
            .from('users')
            .select('id')
            .eq('role', filters.authorRole); // Aquí filtramos en la tabla 'users' directamente

          if (usersError) {
            console.error('Error al obtener IDs de usuarios por rol:', usersError.message);
            throw usersError;
          }

          const userIdsWithRole = usersWithRole.map(user => user.id);
          
          if (userIdsWithRole.length > 0) {
            query = query.in('user_id', userIdsWithRole); // Filtra los posts por esos IDs
          } else {
            // Si no hay usuarios con ese rol, no debería mostrar posts, 
            // así que forzamos un resultado vacío para evitar cargar todos los posts.
            this.posts = [];
            this.loading = false;
            return; 
          }
        }
        // **********************************************

        query = query.order('created_at', { ascending: false });

        const { data, error } = await query;

        if (error) throw error;

        this.posts = data.map(post => {
          // Calcular el promedio de ratings para cada post
          const totalRating = post.ratings.reduce((sum, r) => sum + r.rating, 0);
          const averageRating = post.ratings.length > 0 ? totalRating / post.ratings.length : 0;

          // Encontrar la calificación del usuario actual para este post
          // Busca en `post.ratings` si hay una calificación de `currentUserId`
          const currentUserRating = post.ratings.find(
            rating => rating.user_id === currentUserId
          );
          
          return {
            ...post,
            average_rating: averageRating,
            user_rating: currentUserRating ? currentUserRating.rating : 0 // ¡AQUÍ ESTÁ LA CORRECCIÓN!
          };
        });

      } catch (err) {
        this.error = err.message;
        console.error('Error fetching posts:', err.message);
      } finally {
        this.loading = false;
      }
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