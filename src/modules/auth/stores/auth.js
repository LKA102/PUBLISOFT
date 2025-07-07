// src/modules/auth/stores/auth.js

import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase'; // Asegúrate de que esta ruta es correcta

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null, // Contendrá el objeto de usuario de Supabase Auth y los datos de tu tabla 'users'
    loading: true, // Indica si el estado general de autenticación está cargándose (sesión + perfil)
    error: null, // Para manejar errores específicos
    // profileLoading: false, // Ya no es estrictamente necesario si 'loading' lo abarca
  }),

  actions: {
    /**
     * @description Inicializa el estado de autenticación y carga el perfil completo.
     * Esta es la función principal que se llamará al inicio de la aplicación.
     */
    async initializeAuth() {
      this.loading = true; // Aseguramos que el estado de carga es true al inicio
      this.error = null;
      try {
        console.log('AuthStore: initializeAuth - Obteniendo sesión de Supabase...');
        const { data: { user } } = await supabase.auth.getUser(); 
        
        // Delegamos la lógica de actualización del usuario y carga del perfil a setUser
        await this.setUser(user); 
        
        console.log('AuthStore: initializeAuth - Finalizado. User:', this.user);
      } catch (err) {
        this.error = err.message;
        this.user = null; // En caso de error, aseguramos que no haya usuario
        console.error('AuthStore: Error al inicializar autenticación o cargar perfil:', err.message);
      } finally {
        this.loading = false; // Importante: el proceso de inicialización ha terminado
      }
    },

    /**
     * @description Establece el usuario en el estado y, opcionalmente, carga su perfil completo.
     * Llamada por onAuthStateChange o initializeAuth.
     * @param {object | null} userObj Objeto de usuario de Supabase Auth (puede ser null para logout).
     */
    async setUser(userObj) {
      // Si no hay userObj, es un logout o usuario no autenticado
      if (!userObj) {
        if (this.user !== null) { // Solo si había un usuario antes, limpiar
          this.user = null;
          console.log('AuthStore: Usuario limpiado (setUser con null).');
        }
        return;
      }

      // Si el ID del usuario no ha cambiado Y ya tiene la propiedad 'role' (significa perfil cargado)
      // Evitamos recargar el perfil si ya lo tenemos.
      if (this.user?.id === userObj.id && this.user?.role) {
        console.log('AuthStore: setUser - Usuario ya cargado con perfil completo, omitiendo re-fetch.');
        return;
      }

      // Si es un nuevo usuario, o un usuario existente sin su perfil completo (ej. refresco de token)
      console.log('AuthStore: setUser - detecta cambio/perfil incompleto. Cargando perfil...');
      // Establecemos el usuario básico primero, luego lo enriqueceremos
      this.user = userObj; 
      await this.fetchUserProfile(userObj.id);
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
        
        // Usa setUser para actualizar el estado del store, incluyendo la carga del perfil
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
            // 1. Validar el dominio del email
        //if (!email.endsWith('@unmsm.edu.pe')) {
       //   throw new Error('Dominio de correo inválido. Solo se permiten correos de @unmsm.edu.pe');
       // }
        //console.log('Dominio de email válido.');

        // 2. Verificar el código institucional en la tabla 'verifications'
        //console.log('Verificando código institucional...');
        //const { data: verificationData, error: verificationError } = await supabase
          //.from('verifications')
          //.select('valid')
          //.eq('code', code)
          //.eq('email', email)
          //.single();

        //if (verificationError) {
        //  throw new Error(`Error al verificar código institucional: ${verificationError.message}`);
        //}
        //if (!verificationData || !verificationData.valid) {
        //  throw new Error('Código institucional o correo electrónico inválido(s) o ya utilizado(s).');
        //}
        //console.log('Código institucional verificado y válido.');
            
            const { data: authData, error: authError } = await supabase.auth.signUp({
                email,
                password,
            });

            if (authError) {
                throw new Error(`AuthStore: Error al registrar en Supabase Auth: ${authError.message}`);
            }

            if (authData.user) {
                const { data: userData, error: userError } = await supabase
                    .from('users')
                    .insert([{
                        id: authData.user.id,
                        email: authData.user.email,
                        role: role,
                        alias: alias,
                        avatar_url: " ", // Puedes poner un valor por defecto
                    }])
                    .select()
                    .single();

                if (userError) {
                    throw new Error(`AuthStore: Error al insertar en la tabla 'users': ${userError.message}`);
                }
                console.log('AuthStore: register - Insertado en tabla users:', userData);

                // Después de la creación de un nuevo usuario, actualizamos el store
                // con el usuario básico y luego con su perfil completo.
                // Usamos setUser para asegurar que la info del perfil se obtiene.
                await this.setUser(authData.user);

                if (role === 'student') {
                    const { error: studentError } = await supabase
                        .from('students')
                        .insert([{ user_id: authData.user.id, code: code }]);
                    if (studentError) throw new Error(`AuthStore: Error al insertar en 'students': ${studentError.message}`);
                    console.log('AuthStore: register - Insertado en tabla students.');
                } else if (role === 'admin') {
                    const { error: adminError } = await supabase
                        .from('admins')
                        .insert([{ user_id: authData.user.id }]);
                    if (adminError) throw new Error(`AuthStore: Error al insertar en 'admins': ${adminError.message}`);
                    console.log('AuthStore: register - Insertado en tabla admins.');
                }

                // Descomenta si usas la tabla 'verifications'
                /*
                const { error: updateVerificationError } = await supabase
                    .from('verifications')
                    .update({ valid: false })
                    .eq('code', code)
                    .eq('email', email);
                if (updateVerificationError) console.warn('AuthStore: No se pudo actualizar verificación:', updateVerificationError.message);
                */

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
      // this.profileLoading = true; // No lo necesitamos si 'loading' es el estado global
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

        // Combina la información de Supabase Auth (this.user) con los datos del perfil
        // Asegúrate de que this.user ya tiene la info básica del usuario antes de esta línea
        if (this.user) {
          this.user = { ...this.user, ...data };
        } else {
          // Esto debería ser un caso de borde, pero si this.user es null, crearlo
          this.user = data; 
        }

        if (data.students && data.students.length > 0) {
          this.user.code = data.students[0].code;
        }
        console.log('AuthStore: fetchUserProfile - Perfil de usuario cargado y combinado:', this.user);
      } catch (err) {
        this.error = err.message;
        console.error('AuthStore: Error al cargar el perfil del usuario:', err.message);
        // Podrías decidir limpiar el usuario si el perfil es crítico para la experiencia
        // this.user = null; 
      } finally {
        // this.profileLoading = false; // No lo necesitamos
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
        this.user = null; // Limpiar el estado del usuario
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
  },

  getters: {
    // Solo es autenticado si hay un usuario, tiene un ID Y tiene un rol (significa que el perfil está cargado)
    isAuthenticated: (state) => !!state.user && !!state.user.id && !!state.user.role, 
    isAdmin: (state) => state.user?.role === 'admin',
    // La aplicación está cargando el estado de autenticación (sesión o perfil)
    isAuthLoading: (state) => state.loading, 
  }
});