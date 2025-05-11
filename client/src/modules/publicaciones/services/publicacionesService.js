import * as pdfConverter from './pdfConverter';

const STORAGE_KEY = 'publisoft_publicaciones';

let cache = null; // Cache en memoria para reducir acceso a localStorage

function getData() {
  if (!cache) {
    const rawData = localStorage.getItem(STORAGE_KEY);
    cache = rawData ? JSON.parse(rawData) : [];
  }
  return cache;
}

let saveTimeout = null; 
function saveData(data) {
  cache = [...data];
  if (!saveTimeout) {  
    saveTimeout = setTimeout(() => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      saveTimeout = null; 
    }, 500);
  }
}


export const publicacionesService = {
  async subir({ titulo, archivo, usuario }) {
    const publicaciones = getData();
    const id = Date.now().toString();
    
    try {
      // Convertir a PDF
      const pdfBlob = await pdfConverter.convertToPDF(archivo);
      const pdfUrl = URL.createObjectURL(pdfBlob);
      
      // Generar vista previa
      const previewUrl = await pdfConverter.generateThumbnail(pdfBlob);
      
      const nueva = {
        id,
        titulo: titulo || 'Apuntes sin título',
        archivoUrl: pdfUrl,
        previewUrl,
        usuario,
        fecha: new Date(),
        rating: 0,
        votos: 0,
        tipo: archivo.type,
        nombreOriginal: archivo.name
      };
      
      publicaciones.push(nueva);
      saveData(publicaciones);
      return nueva;
    } catch (error) {
      console.error('Error en subir publicación:', error);
      throw error;
    }
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