// src/modules/admin/stores/admin.js
import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase'; // Asegúrate de la ruta correcta a tu instancia de Supabase

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [], // Para la lista de usuarios en la tabla
    verificationCodes: [],
    loading: false,
    error: null,
    // ESTADOS PARA MÉTRICAS
    totalUsers: 0, // Contará el total de usuarios
    totalPosts: 0,
    totalUnusedCodes: 0,
    totalStudents: 0, // Asegúrate de haberlo añadido en el state si lo vas a usar
  }),

  actions: {
    // Acción para cargar la LISTA completa de usuarios para la tabla
    async fetchAllUsers() {
      this.loading = true;
      this.error = null;
      try {
        // Al seleccionar, no necesitas el 'count' si solo quieres la lista de datos.
        // El conteo se hará en 'fetchTotalUsers'.
        const { data, error } = await supabase
          .from('users')
          .select('id, alias, email, role, created_at'); 

        if (error) throw error;
        this.users = data || [];
        console.log('AdminStore: Usuarios cargados para la lista:', this.users);
      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Error fetching all users:', err.message);
      } finally {
        this.loading = false;
      }
    },

    async deleteUser(userId) {
      this.loading = true;
      this.error = null;
      try {
        // ---- ADVERTENCIA DE SEGURIDAD CRÍTICA ----
        // Las siguientes operaciones se realizan directamente desde el cliente.
        // La eliminación de 'auth.users' con supabase.auth.admin.deleteUser
        // casi siempre requerirá una 'service_role' key, la cual NO DEBE
        // exponerse en el frontend. Si esto funciona, es porque has expuesto
        // una clave de API con privilegios elevados o has configurado políticas
        // RLS EXTREMADAMENTE permisivas, lo cual NO ES SEGURO para producción.
        // Se recomienda enfáticamente usar una Edge Function o un trigger de PostgreSQL
        // para estas operaciones en un entorno real.
        // ------------------------------------------

        // 1. Eliminar de la tabla 'students'
        console.log(`Attempting to delete from 'students' for userId: ${userId}`);
        const { error: studentError } = await supabase
          .from('students')
          .delete()
          .eq('user_id', userId); 

        if (studentError) {
          console.error('Error deleting from students table:', studentError);
          throw new Error(`Failed to delete from students table: ${studentError.message}`);
        }
        console.log('Deleted from students table successfully.');

        // 2. Eliminar de la tabla 'users'
        console.log(`Attempting to delete from 'users' table for userId: ${userId}`);
        const { error: userTableError } = await supabase
          .from('users')
          .delete()
          .eq('id', userId);

        if (userTableError) {
          console.error('Error deleting from users table:', userTableError);
          throw new Error(`Failed to delete from users table: ${userTableError.message}`);
        }
        console.log('Deleted from users table successfully.');
        
        // 3. Opcional: Eliminar de Supabase Authentication (auth.users)
        // Como se mencionó, esta parte es muy probable que falle desde el cliente
        // sin la service_role key o una función de servidor.
        // Lo comento de nuevo para evitar que cause errores si no está configurado de forma segura.
        /*
        console.log(`Attempting to delete from Supabase Auth (auth.users) for userId: ${userId}`);
        const { error: authError } = await supabase.auth.admin.deleteUser(userId);
        if (authError) {
          console.error('Error deleting from auth.users (authentication):', authError);
          throw new Error(`Failed to delete user from authentication: ${authError.message}. This operation usually requires a server-side context (e.g., Edge Function) with service_role key.`);
        }
        console.log('Deleted from auth.users successfully.');
        */

        // Si la eliminación en la base de datos fue exitosa, actualiza el estado local
        this.users = this.users.filter(user => user.id !== userId);
        // Llama a fetchTotalUsers para recalcular el conteo después de la eliminación
        await this.fetchTotalUsers(); 
        alert('Usuario y datos asociados eliminados con éxito.');

      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Global Error during user deletion:', err.message);
        alert(`Error al eliminar usuario: ${err.message}. Revisa la consola para más detalles.`);
      } finally {
        this.loading = false;
      }
    },

    async fetchVerificationCodes() {
      this.loading = true;
      this.error = null;
      try {
        const { data, error, count } = await supabase
          .from('verifications')
          .select('code, email', { count: 'exact' })
          .order('code', { ascending: true });

        if (error) throw error;
        this.verificationCodes = data || [];
        this.totalUnusedCodes = data.length; 
        console.log('AdminStore: Códigos de verificación cargados:', this.verificationCodes, 'Total:', this.totalUnusedCodes);
      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Error fetching verification codes:', err.message);
      } finally {
        this.loading = false;
      }
    },

    async deleteVerificationCode(codeValue) {
      this.loading = true;
      this.error = null;
      try {
        const { error } = await supabase
          .from('verifications')
          .delete()
          .eq('code', codeValue);

        if (error) throw error;
        this.verificationCodes = this.verificationCodes.filter(code => code.code !== codeValue);
        this.totalUnusedCodes = this.verificationCodes.length; 
        alert('Código de verificación eliminado con éxito.');
      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Error deleting verification code:', err.message);
        alert(`Error al eliminar código: ${err.message}`);
      } finally {
        this.loading = false;
      }
    },

    async fetchTotalPosts() {
      this.loading = true;
      this.error = null;
      try {
        const { count, error } = await supabase
          .from('posts')
          .select('*', { count: 'exact', head: true }); 

        if (error) throw error;
        this.totalPosts = count || 0;
        console.log('AdminStore: Total de publicaciones:', this.totalPosts);
      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Error fetching total posts:', err.message);
      } finally {
        this.loading = false;
      }
    },

    // Acción para OBTENER EL CONTEO TOTAL de usuarios
    async fetchTotalUsers() { // Renombré esta acción para mayor claridad
      this.loading = true;
      this.error = null;
      try {
        const { count, error } = await supabase
          .from('users')
          .select('*', { count: 'exact', head: true }); // Usamos head: true para obtener solo el conteo

        if (error) throw error;
        this.totalUsers = count || 0;
        console.log('AdminStore: Total de usuarios:', this.totalUsers);
      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Error fetching total users count:', err.message); // Consola más específica
      } finally {
        this.loading = false;
      }
    },

    // NUEVA ACCIÓN: Obtener el total de estudiantes
    async fetchTotalStudents() {
      this.loading = true;
      this.error = null;
      try {
        const { count, error } = await supabase
          .from('students') // Asegúrate de que esta es la tabla correcta para los estudiantes
          .select('*', { count: 'exact', head: true }); // Solo para obtener el conteo

        if (error) throw error;
        this.totalStudents = count || 0;
        console.log('AdminStore: Total de estudiantes:', this.totalStudents);
      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Error fetching total students:', err.message);
      } finally {
        this.loading = false;
      }
    },

    // Acción para cargar todas las métricas al inicio
    async fetchAllMetrics() {
      this.loading = true;
      this.error = null;
      try {
        await Promise.all([
          // Llama a las acciones de CONTEO
          this.fetchTotalUsers(), // Llama a la acción que obtiene solo el conteo de usuarios
          this.fetchTotalPosts(),
          this.fetchTotalStudents(),
          this.fetchVerificationCodes(), // Esto ya actualiza totalUnusedCodes al traer los códigos
          // this.fetchAllUsers(), // Solo llama a esta si necesitas poblar la tabla de usuarios en el dashboard al inicio
        ]);
      } catch (err) {
        this.error = err.message;
        console.error('AdminStore: Error fetching all metrics:', err.message);
      } finally {
        this.loading = false;
      }
    },
  },
});