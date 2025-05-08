// // src/modules/publicaciones/services/publicacionesService.js
// let publicaciones = [];

// export const publicacionesService = {
//   async subir({ titulo, archivo, usuario }) {
//     const id = Date.now().toString();
//     const nueva = {
//       id,
//       titulo,
//       archivoUrl: URL.createObjectURL(archivo),
//       usuario,
//       fecha: new Date(),
//       rating: 0,
//       votos: 0,
//     };
//     publicaciones.push(nueva);
//     return nueva;
//   },

//   async eliminar(id) {
//     publicaciones = publicaciones.filter(p => p.id !== id);
//   },

//   async calificar(id, estrellas) {
//     const pub = publicaciones.find(p => p.id === id);
//     if (pub) {
//       pub.rating = ((pub.rating * pub.votos) + estrellas) / (pub.votos + 1);
//       pub.votos += 1;
//     }
//   },

//   async obtenerTendencias() {
//     return [...publicaciones].sort((a, b) => (b.rating + b.votos) - (a.rating + a.votos));
//   }
// };


// src/modules/publicaciones/services/publicacionesService.js

const STORAGE_KEY = 'publisoft_publicaciones';

function getData() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
}

function saveData(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export const publicacionesService = {
  async subir({ titulo, archivo, usuario }) {
    const publicaciones = getData();
    const id = Date.now().toString();
    const nueva = {
      id,
      titulo,
      archivoUrl: URL.createObjectURL(archivo),
      usuario,
      fecha: new Date(),
      rating: 0,
      votos: 0,
    };
    publicaciones.push(nueva);
    saveData(publicaciones);
    return nueva;
  },

  async eliminar(id) {
    let publicaciones = getData();
    publicaciones = publicaciones.filter(p => p.id !== id);
    saveData(publicaciones);
  },

  async calificar(id, estrellas) {
    const publicaciones = getData();
    const pub = publicaciones.find(p => p.id === id);
    if (pub) {
      pub.rating = ((pub.rating * pub.votos) + estrellas) / (pub.votos + 1);
      pub.votos += 1;
      saveData(publicaciones);
    }
  },

  async obtenerTendencias() {
    return getData().sort((a, b) => (b.rating + b.votos) - (a.rating + a.votos));
  }
};
