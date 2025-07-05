import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase'; // Asegúrate de que esta ruta sea correcta para tu configuración
import router from '@/router'; // <--- Asegúrate de importar tu instancia de Vue Router aquí

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null, // Contendrá el objeto de usuario de Supabase Auth y los datos de tu tabla 'users'
    loading: false, // Para manejar estados de carga en la UI
    error: null, // Para manejar errores específicos
  }),

  actions: {
    /**
     * @description Inicia sesión de un usuario con email y contraseña.
     * @param {string} email
     * @param {string} password
     */
    async login(email, password) {
      this.loading = true;
      this.error = null;
      try {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });

        if (error) {
          throw error; // Lanza el error para ser capturado en el catch
        }

        this.user = data.user;
        // Opcional: Cargar el perfil completo del usuario desde tus tablas
        if (this.user) {
          await this.fetchUserProfile(this.user.id);
        }
        console.log('Usuario logueado:', this.user);
        alert('¡Inicio de sesión exitoso!');
        if (router) { // Verificamos que router esté importado y disponible
          router.push('/feed'); // <--- Esta línea es la clave para la redirección
        } else {
          console.warn("Vue Router no está disponible para redirección. Asegúrate de que '@/router' se importe correctamente.");
        }
      } catch (err) {
        this.error = err.message;
        console.error('Error al iniciar sesión:', err.message);
        alert('Error al iniciar sesión: ' + err.message);
      } finally {
        this.loading = false;
      }
    },

    /**
     * @description Registra un nuevo usuario, verifica el código institucional e inserta en tablas personalizadas.
     * @param {string} email
     * @param {string} code Código institucional
     * @param {string} password
     * @param {'student' | 'admin'} [role='student'] Rol del usuario a registrar
     */
    async register(email, code, password, alias, role = 'student') {
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

        // 3. Registrar usuario en Supabase Auth
        console.log('Registrando usuario en Supabase Auth...');
        const { data: authData, error: authError } = await supabase.auth.signUp({
          email,
          password,
        });

        if (authError) {
          throw new Error(`Error al registrar en Supabase Auth: ${authError.message}`);
        }

        this.user = authData.user;
        console.log('Usuario registrado en Supabase Auth:', this.user);

        // Si el usuario se creó en auth.users, proceder a insertar en tus tablas personalizadas
        if (this.user) {
          // 4. Insertar en la tabla 'users'
          console.log('Intentando insertar en la tabla users...');
          const { data: userData, error: userError } = await supabase
            .from('users')
            .insert([
              {
                id: this.user.id, // Usar el ID de Supabase Auth
                email: this.user.email,
                role: role,
                alias: alias, // Guardar el alias proporcionado
                //avatar_url: defaultAvatarUrl, 
                // Puedes añadir 'alias' aquí si lo tienes en el formulario de registro
              },
            ])
            .select()
            .single();

          if (userError) {
            // Si falla la inserción en 'users', deberías considerar eliminar el usuario de Supabase Auth
            // Esto es complejo y requiere permisos de servicio o una función Edge para ser seguro.
            // Por simplicidad, por ahora, solo lanzamos el error.
            throw new Error(`Error al insertar en la tabla 'users': ${userError.message}`);
          }
          console.log('Insertado en tabla users:', userData);

          // 5. Insertar en la tabla de rol específica ('students' o 'admins')
          if (role === 'student') {
            console.log('Intentando insertar en la tabla students...');
            const { error: studentError } = await supabase
              .from('students')
              .insert([{ user_id: this.user.id, code: code }]); // Usar el 'code' para la tabla 'students'

            if (studentError) {
              throw new Error(`Error al insertar en la tabla 'students': ${studentError.message}`);
            }
            console.log('Insertado en tabla students.');
          } else if (role === 'admin') {
            console.log('Intentando insertar en la tabla admins...');
            const { error: adminError } = await supabase
              .from('admins')
              .insert([{ user_id: this.user.id }]);

            if (adminError) {
              throw new Error(`Error al insertar en la tabla 'admins': ${adminError.message}`);
            }
            console.log('Insertado en tabla admins.');
          }

          // 6. Marcar el código de verificación como inválido después de usarlo
          console.log('Actualizando estado de verificación del código...');
          const { error: updateVerificationError } = await supabase
            .from('verifications')
            .update({ valid: false })
            .eq('code', code)
            .eq('email', email);

          if (updateVerificationError) {
            console.warn('Advertencia: No se pudo actualizar el estado de verificación del código:', updateVerificationError.message);
          } else {
            console.log('Estado de verificación actualizado a inválido.');
          }

          alert('¡Registro exitoso! Por favor, verifica tu correo electrónico.');
        }

      } catch (err) {
        this.error = err.message;
        console.error('Error durante el proceso de registro:', err.message);
        alert('Error en el registro: ' + err.message);
      } finally {
        this.loading = false;
      }
    },

    /**
     * @description Carga el perfil completo del usuario desde tus tablas personalizadas.
     * @param {string} userId El ID del usuario de Supabase Auth.
     */
    async fetchUserProfile(userId) {
      this.loading = true;
      this.error = null;
      try {
        const { data, error } = await supabase
          .from('users')
          .select('*, students(code), admins(*)') // Trae datos de 'users' y relaciona con 'students' o 'admins'
          .eq('id', userId)
          .single();

        if (error) {
          throw error;
        }

        // Combina la información de Supabase Auth (this.user ya tiene email, id, etc.) con los datos de tu tabla 'users'
        this.user = { ...this.user, ...data };

        // Si es un estudiante, el campo 'code' estará en data.students[0].code
        if (data.students && data.students.length > 0) {
          this.user.code = data.students[0].code;
        }
        console.log('Perfil de usuario cargado:', this.user);
      } catch (err) {
        this.error = err.message;
        console.error('Error al cargar el perfil del usuario:', err.message);
        // Si hay un error crítico al cargar el perfil, podrías querer limpiar el usuario
        // this.user = null;
      } finally {
        this.loading = false;
      }
    },

    /**
     * @description Cierra la sesión del usuario actual.
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
        console.log('Sesión cerrada.');
        alert('¡Sesión cerrada exitosamente!');
      } catch (err) {
        this.error = err.message;
        console.error('Error al cerrar sesión:', err.message);
        alert('Error al cerrar sesión: ' + err.message);
      } finally {
        this.loading = false;
      }
    },

    /**
     * @description Establece el usuario en el estado. Útil para inicializar el store
     * cuando se detecta una sesión existente al cargar la aplicación.
     * @param {object} userObj Objeto de usuario de Supabase Auth.
     */
    setUser(userObj) {
      this.user = userObj;
      if (userObj) {
        // Cargar el perfil completo al iniciar la app si hay una sesión activa
        this.fetchUserProfile(userObj.id);
      }
    },
  },
});