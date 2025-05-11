<template>
  <div class="cabecera">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    
    <div class="usuario">
      <div class="notificaciones" @click="mostrarNotificaciones = !mostrarNotificaciones">
        <v-badge color="red" :content="notificaciones.length" overlap>
          <v-icon>mdi-bell</v-icon>
        </v-badge>
        <span>Notificaciones</span>
      </div>

      <div class="perfil">
        <span>Stefano H.</span>
        <v-avatar size="36">
          <img src="@/assets/perfil.jpg" alt="Perfil" />
        </v-avatar>
      </div>
    </div>

    <!-- Panel de notificaciones -->
    <div v-if="mostrarNotificaciones" class="panel-notificaciones">
      <div class="encabezado">
        <span>Notificaciones</span>
        <v-icon @click="mostrarNotificaciones = false" class="cerrar">mdi-close</v-icon>
      </div>
      <v-card
        v-for="(n, i) in notificaciones"
        :key="i"
        class="notificacion"
      >
        <v-card-text>{{ n.texto }}</v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Cabecera',
  data() {
    return {
      mostrarNotificaciones: false,
      notificaciones: [
        {
          texto: '🔔 5 estudiantes reaccionaron a tu apunte “Resumen de Álgebra”:\n2 dijeron “Muy útil”, 2 “Me salvó” y 1 “Buen resumen”'
        },
        {
          texto: 'German reaccionó a tu apunte con “📘 Buen resumen”'
        },
        {
          texto: 'German le dio 5 estrellas ⭐⭐⭐⭐⭐ a tu apunte.'
        },
        {
          texto: 'Lucía dejó una valoración de 2 estrellas ⭐⭐ en tu apunte.'
        }
      ]
    };
  }
};
</script>

<style scoped>
.cabecera {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #163e88;
  padding: 10px 20px;
  color: white;
}
.logo {
  height: 40px;
}
.usuario {
  display: flex;
  align-items: center;
  gap: 20px;
}
.notificaciones {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.panel-notificaciones {
  position: absolute;
  top: 70px;
  right: 20px;
  width: 350px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 15px;
  z-index: 100;
}
.encabezado {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  margin-bottom: 10px;
}
.notificacion {
  margin-bottom: 10px;
  font-size: 14px;
  white-space: pre-wrap;
}
.cerrar {
  cursor: pointer;
}
</style>
