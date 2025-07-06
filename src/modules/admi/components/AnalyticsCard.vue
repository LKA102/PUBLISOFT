<template>
  <div class="analytics-card">
    <div class="card-icon">
      <i :class="icon"></i>
    </div>
    <div class="card-content">
      <div class="card-value">{{ value }}</div>
      <div class="card-title">{{ title }}</div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  icon: {
    type: String,
    default: 'fas fa-info-circle', // Ícono por defecto si no se especifica
  },
});
</script>

<style scoped>
.analytics-card {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  min-width: 200px;
  flex: 1; /* Permite que las tarjetas se expandan y ocupen espacio */
  margin: 10px; /* Espacio entre tarjetas */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.analytics-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.card-icon {
  font-size: 2.5em;
  color: #007bff; /* Color primario, puedes cambiarlo */
  margin-right: 15px;
  width: 50px; /* Fija el ancho para consistencia */
  text-align: center;
}

.card-icon .fas, .card-icon .far, .card-icon .fab {
  line-height: 1; /* Ajusta la línea para centrar verticalmente */
}

.card-content {
  display: flex;
  flex-direction: column;
}

.card-value {
  font-size: 2.2em;
  font-weight: bold;
  color: #343a40;
  margin-bottom: 5px;
}

.card-title {
  font-size: 1.1em;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Opcional: Estilos para diferentes colores de íconos/cards según el tipo */
.analytics-card.users .card-icon { color: #28a745; } /* Verde */
.analytics-card.posts .card-icon { color: #fd7e14; } /* Naranja */
.analytics-card.verifications .card-icon { color: #17a2b8; } /* Turquesa */
.analytics-card.ratings .card-icon { color: #ffc107; } /* Amarillo */
</style>