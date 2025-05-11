<template>
  <div class="cabecera">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    
    <div class="usuario">
      <div class="notificaciones" @click="mostrarNotificaciones = !mostrarNotificaciones">
        <div class="numero-notificaciones">
          <span>4</span>
        </div>
        <span>Notificaciones</span>
      </div>

      <v-divider vertical thickness="3" color = "grey" opacity="100" ></v-divider>
      <div class="perfil">
        <span>Stefano H.</span>
        <v-avatar size="36">
          <img src="@/assets/perfil.jpg" alt="Perfil" />
        </v-avatar>
      </div>
    </div>

    <!-- Modal de notificaciones -->
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
  padding: 10px 30px;
  background-color: white;
  border-radius: 999px;
  color: #1E3984;


}
.notificaciones {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 10px;
}

.numero-notificaciones{
  background-color: #E47579;
  color: white;
  border-radius: 999px;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.perfil {
  display: flex;
  align-items: center;
  gap: 10px;
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
  color: #1E3984;
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
