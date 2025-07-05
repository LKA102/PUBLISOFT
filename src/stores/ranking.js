// src/stores/ranking.js
import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase';

export const useRankingStore = defineStore('ranking', {
  state: () => ({
    currentRanking: [],
    monthlyHistory: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchCurrentRanking() {
      this.loading = true;
      this.error = null;
      try {
        const { data, error } = await supabase.rpc('get_student_ranking');
        if (error) throw error;
        this.currentRanking = data;
        console.log('Ranking actual:', this.currentRanking);
      } catch (err) {
        this.error = err.message;
        console.error('Error al cargar el ranking actual:', err.message);
      } finally {
        this.loading = false;
      }
    },

    async fetchMonthlyHistory() {
      this.loading = true;
      this.error = null;
      try {
        const { data, error } = await supabase
          .from('monthly_rankings_history')
          .select(`
            id,
            month_year,
            top_score,
            users (
              alias,
              avatar_url
            )
          `)
          .order('month_year', { ascending: false }) // Mostrar el más reciente primero
          .limit(12); // Opcional: limitar el historial a los últimos 12 meses

        if (error) throw error;
        this.monthlyHistory = data;
        console.log('Historial de rankings mensuales:', this.monthlyHistory);
      } catch (err) {
        this.error = err.message;
        console.error('Error al cargar el historial de rankings:', err.message);
      } finally {
        this.loading = false;
      }
    },

    async saveMonthlyTopStudent() {
      this.loading = true;
      this.error = null;
      try {
        const { data, error } = await supabase.rpc('save_monthly_top_student');

        if (error) throw error;

        // La función RPC ahora devuelve TRUE o FALSE si no hay estudiantes.
        if (data === false) {
             console.log('Monthly top student update declined by DB function (e.g., no top student).');
             this.loading = false;
             return false;
        }

        console.log('Monthly top student saved/updated successfully:', data);
        await this.fetchMonthlyHistory(); // Recargar el historial para ver el cambio
        // No alertamos cada vez, ya que esto se hará a menudo
        return true;

      } catch (err) {
        this.error = err.message;
        console.error('Error al guardar/actualizar el estudiante del mes:', err.message);
        // Si hay un error al sobrescribir, es un problema real, lo mostramos
        alert(`Error al guardar/actualizar el ranking: ${err.message}`);
        return false;
      } finally {
        this.loading = false;
      }
    },
  },
});