<template>
  <div class="notificaciones-container">
    <Cabecera />
    <div class="contenido-notificaciones">
    </div>
  </div>
</template>

<script>
import Cabecera from "@/modules/notificaciones/componentes/cabecera.vue";

export default {
  name: "Notificaciones",
  components: {
    Cabecera
  }
};
</script>

<style scoped>
.notificaciones-container {
  width: 100%; /* Asegura que ocupe todo el ancho */
  background-color: white; /* Fondo blanco */
  min-height: 100vh; /* Asegura que ocupe toda la altura de la pantalla */
}

.contenido-notificaciones {
  padding: 20px; /* Agrega algo de espacio alrededor del contenido */
}
</style>
