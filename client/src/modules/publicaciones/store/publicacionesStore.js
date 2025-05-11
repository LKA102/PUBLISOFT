// src/modules/publicaciones/store/publicacionesStore.js
import { reactive } from 'vue';
import { publicacionesService } from '../services/publicacionesService';

const state = reactive({
  publicaciones: [],
});

export const usePublicaciones = () => {
 // DESPUÉS (Green Software)
  let lastUpdate = 0;

  const cargar = async () => {
    // Evita recargas frecuentes (mínimo 30 segundos entre actualizaciones)
    const now = Date.now();
    if (now - lastUpdate < 30000 && state.publicaciones.length > 0) return;
    
    state.publicaciones = await publicacionesService.obtenerTendencias();
    lastUpdate = now;
    
  };

  const subir = async (datos) => {
  await publicacionesService.subir(datos);
  state.publicaciones = [...await publicacionesService.obtenerTendencias()]; 
  };

  const eliminar = async (id) => {
    await publicacionesService.eliminar(id);
    await cargar();
  };

  const calificar = async (id, estrellas) => {
    await publicacionesService.calificar(id, estrellas);
    await cargar();
  };

  return { state, cargar, subir, eliminar, calificar };
};
