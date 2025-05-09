// src/modules/publicaciones/store/publicacionesStore.js
import { reactive } from 'vue';
import { publicacionesService } from '../services/publicacionesService';

const state = reactive({
  publicaciones: [],
});

export const usePublicaciones = () => {
  const cargar = async () => {
    state.publicaciones = await publicacionesService.obtenerTendencias();
  };

  const subir = async (datos) => {
    await publicacionesService.subir(datos);
    await cargar();
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
