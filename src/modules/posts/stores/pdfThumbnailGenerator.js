// src/utils/pdfThumbnailGenerator.js
import * as pdfjsLib from 'pdfjs-dist';

// Configura la ruta a los workers de PDF.js. Esto es CRUCIAL.
// Puedes copiarlos a tu directorio public o servir desde un CDN.
// Para un entorno de desarrollo de Vue, puedes apuntar a los archivos en node_modules:
pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.mjs'; // <--- CAMBIO AQUÍ

// Función principal para generar una miniatura de la primera página de un PDF
export async function generatePdfThumbnail(pdfFileBlob, scale = 0.5) {
  console.log('Iniciando generación de miniatura PDF con PDF.js (Wasm)...');
  const startTime = performance.now();

  try {
    const arrayBuffer = await pdfFileBlob.arrayBuffer();
    const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
    const pdf = await loadingTask.promise;

    // Obtener la primera página
    const page = await pdf.getPage(1);

    // Calcular el viewport a la escala deseada
    const viewport = page.getViewport({ scale: scale });

    // Crear un elemento canvas para renderizar
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Renderizar la página en el canvas
    await page.render({ canvasContext: context, viewport: viewport }).promise;

    // Convertir el contenido del canvas a un Blob (JPG)
    const thumbnailBlob = await new Promise(resolve => {
      canvas.toBlob(blob => {
        resolve(blob);
      }, 'image/jpeg', 0.8); // Formato JPEG con calidad 80%
    });

    const endTime = performance.now();
    console.log(`Miniatura PDF generada en ${(endTime - startTime).toFixed(2)} ms`);

    return {
      thumbnailBlob,
      processingTime: (endTime - startTime),
      originalSize: pdfFileBlob.size,
      processedSize: thumbnailBlob.size
    };

  } catch (error) {
    console.error('Error al generar miniatura PDF:', error);
    throw new Error('No se pudo generar la miniatura del PDF.');
  }
}

// Función de utilidad para formatear bytes a un formato legible
export const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};