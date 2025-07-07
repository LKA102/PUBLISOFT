// src/modules/auth/stores/auth.js

import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase'; 

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null, 
    loading: true, 
    error: null, 
    needsRating: false, 
  }),

  // Todas las funciones que modifican el estado o realizan operaciones asíncronas deben ir aquí.
  actions: {
    /**
     * @description Inicializa el estado de autenticación y carga el perfil completo.
     * Esta es la función principal que se llamará al inicio de la aplicación.
     */
    async initializeAuth() {
      this.loading = true; 
      this.error = null;
      try {
        console.log('AuthStore: initializeAuth - Obteniendo sesión de Supabase...');
        const { data: { user } = {} } = await supabase.auth.getUser(); // Añadir {} por si data es null/undefined
        await this.setUser(user); 
        console.log('AuthStore: initializeAuth - Finalizado. User:', this.user);
      } catch (err) {
        this.error = err.message;
        this.user = null; 
        this.needsRating = false; 
        console.error('AuthStore: Error al inicializar autenticación o cargar perfil:', err.message);
      } finally {
        this.loading = false; 
      }
    },

    /**
     * @description Establece el usuario en el estado y, opcionalmente, carga su perfil completo.
     * Llamada por onAuthStateChange o initializeAuth.
     * @param {object | null} userObj Objeto de usuario de Supabase Auth (puede ser null para logout).
     */
    async setUser(userObj) {
      if (!userObj) {
        if (this.user !== null) { 
          this.user = null;
          this.needsRating = false;
          console.log('AuthStore: Usuario limpiado (setUser con null).');
        }
        return;
      }

      const currentUserId = this.user?.id;
      const currentEnrichedRole = this.user?.role && this.user.role !== 'authenticated';
      const incomingUserId = userObj.id;

      if (!currentUserId || currentUserId !== incomingUserId || !currentEnrichedRole) {
        console.log('AuthStore: setUser - Detecta necesidad de cargar/refrescar perfil completo.');
        this.user = { ...userObj }; // Establece el usuario básico de Supabase Auth
        await this.fetchUserProfile(userObj.id); // Carga y fusiona el perfil enriquecido
      } else {
        console.log('AuthStore: setUser - Usuario ya cargado con perfil completo, solo actualizando datos de sesión.');
        // Actualizamos las propiedades básicas del userObj entrante, pero EXCLUIMOS 'role'
        // para que no sobrescriba nuestro rol enriquecido si ya lo tenemos.
        const { role: incomingRole, ...restOfUserObj } = userObj; // Desestructuramos para excluir 'role'

        this.user = { ...this.user, ...restOfUserObj }; 
        // Si incomingRole es 'authenticated' y this.user.role ya es 'student',
        // queremos mantener 'student'. No lo fusionamos si ya hay un rol enriquecido.
      }

      // SIEMPRE llamar a checkRatingRequirement si el usuario está autenticado y tiene un rol
      if (this.isAuthenticated) { 
        await this.checkRatingRequirement();
      }
    },

    /**
     * @description Inicia sesión de un usuario con email y contraseña.
     * @param {string} email
     * @param {string} password
     * @returns {{ success: boolean, error?: string }}
     */
    async login(email, password) {
      this.loading = true; 
      this.error = null;
      try {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });

        if (error) {
          throw error; 
        }
        
        await this.setUser(data.user); 
        
        console.log('AuthStore: login - Usuario logueado e info actualizada.');
        return { success: true };
      } catch (err) {
        this.error = err.message; 
        console.error('AuthStore: Error al iniciar sesión:', err.message);
        return { success: false, error: err.message }; 
      } finally {
        this.loading = false; 
      }
    },

    /**
     * @description Registra un nuevo usuario...
     * @returns {{ success: boolean, error?: string }}
     */
    async register(email, code, alias, password, role = 'student') {
        this.loading = true;
        this.error = null;
        try {
            const { data: verificationData, error: verificationError } = await supabase
                .from('verifications')
                .select('*')
                .eq('email', email)
                .eq('code', code)
                .eq('valid', true)
                .single();

            if (verificationError || !verificationData) {
                throw new Error('No encontramos tus datos en la base de datos de la Facultad. Verifica tu correo institucional y código.');
            }

            const { data: authData, error: authError } = await supabase.auth.signUp({
              email,
              password,
              options: {
                emailRedirectTo: `${window.location.origin}/login`,
              },
            });

            if (authError) {
                throw new Error(`Error al registrar en Supabase Auth: ${authError.message}`);
            }

            if (authData.user) {
                const { data: userData, error: userError } = await supabase
                    .from('users')
                    .insert([{
                        id: authData.user.id,
                        email: authData.user.email,
                        role: role,
                        alias: alias,
                        avatar_url: " ",
                    }])
                    .select()
                    .single();

                if (userError) {
                    throw new Error(`Error al insertar en la tabla 'users': ${userError.message}`);
                }

                await this.setUser(authData.user);

                if (role === 'student') {
                    const { error: studentError } = await supabase
                        .from('students')
                        .insert([{ user_id: authData.user.id, code: code }]);
                    if (studentError) throw new Error(`Error al insertar en 'students': ${studentError.message}`);
                } else if (role === 'admin') {
                    const { error: adminError } = await supabase
                        .from('admins')
                        .insert([{ user_id: authData.user.id }]);
                    if (adminError) throw new Error(`Error al insertar en 'admins': ${adminError.message}`);
                }

                return { success: true };
            }

        } catch (err) {
            this.error = err.message;
            console.error('AuthStore: Error durante el proceso de registro:', err.message);
            return { success: false, error: err.message };
        } finally {
            this.loading = false;
        }
    },

    /**
     * @description Carga el perfil completo del usuario desde tus tablas personalizadas.
     * @param {string} userId El ID del usuario de Supabase Auth.
     */
    async fetchUserProfile(userId) {
      this.error = null; 
      try {
        console.log('AuthStore: fetchUserProfile - Cargando perfil para userId:', userId);
        const { data, error } = await supabase
          .from('users')
          .select('*, students(code), admins(*)') 
          .eq('id', userId)
          .single();

        if (error) {
          throw error;
        }

        // Importante: No sobrescribir completamente this.user aquí si ya tiene propiedades del perfil enriquecido.
        // Solo fusionar los datos nuevos.
        this.user = { ...this.user, ...data }; 
        
        if (data.students && data.students.length > 0) {
          this.user.code = data.students[0].code;
        }
        console.log('AuthStore: fetchUserProfile - Perfil de usuario cargado y combinado:', this.user);
      } catch (err) {
        this.error = err.message;
        console.error('AuthStore: Error al cargar el perfil del usuario:', err.message);
      }
    },

    /**
     * @description Cierra la sesión del usuario actual.
     * @returns {{ success: boolean, error?: string }}
     */
    async signOut() {
      this.loading = true; 
      this.error = null;
      try {
        const { error } = await supabase.auth.signOut();
        if (error) {
          throw error;
        }
        this.user = null; 
        this.needsRating = false; 
        console.log('AuthStore: Sesión cerrada.');
        return { success: true };
      } catch (err) {
        this.error = err.message;
        console.error('AuthStore: Error al cerrar sesión:', err.message);
        return { success: false, error: err.message };
      } finally {
        this.loading = false; 
      }
    },

    /**
     * @description Verifica si un usuario estudiante ha valorado un post hoy.
     * Actualiza la propiedad `needsRating` del store.
     */
    async checkRatingRequirement() {
        if (!this.user || this.user.role !== 'student') {
            this.needsRating = false;
            return;
        }

        let lastRatingDate = null;
        try {
            const { data: dateData, error: rpcError } = await supabase.rpc('get_user_last_rating_date', { p_user_id: this.user.id });
            
            if (rpcError) {
                console.error('AuthStore: Error al obtener la última fecha de rating desde RPC:', rpcError.message);
                this.needsRating = true; 
                return;
            }

            if (dateData) {
                lastRatingDate = new Date(dateData);
                lastRatingDate.setUTCHours(0, 0, 0, 0); 
            }
        } catch (error) {
            console.error('AuthStore: Error inesperado en checkRatingRequirement:', error.message);
            this.needsRating = true; 
            return;
        }
        
        const today = new Date();
        today.setUTCHours(0, 0, 0, 0); 

        if (!lastRatingDate || lastRatingDate < today) {
            this.needsRating = true;
            console.log('AuthStore: Usuario estudiante necesita valorar un post (último rating: %s).', lastRatingDate ? lastRatingDate.toISOString() : 'nunca');
        } else {
            this.needsRating = false;
            console.log('AuthStore: Usuario estudiante ya valoró un post hoy (último rating: %s).', lastRatingDate.toISOString());
        }
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.user && !!state.user.id && !!state.user.role, 
    isAdmin: (state) => state.user?.role === 'admin',
    isTeacher: (state) => state.user?.role === 'teacher', 
    isStudent: (state) => state.user?.role === 'student', 
    isAuthLoading: (state) => state.loading, 
  }
});