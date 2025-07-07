// src/utils/imageProcessor.js

/**
 * Procesa una imagen para generar una miniatura redimensionada y comprimida.
 * Utiliza el canvas del navegador, que es optimizado.
 * @param {File} imageFileBlob - El objeto File de la imagen original.
 * @param {number} maxWidth - Ancho máximo deseado para la miniatura.
 * @param {number} maxHeight - Alto máximo deseado para la miniatura.
 * @param {number} quality - Calidad de compresión (0 a 1) para JPEG/WebP.
 * @returns {Promise<{processedBlob: Blob, processingTime: number, originalSize: number, processedSize: number}>}
 */
export async function processImageForThumbnail(imageFileBlob, maxWidth = 400, maxHeight = 400, quality = 0.8) {
  console.log('Iniciando procesamiento de imagen para miniatura...');
  const startTime = performance.now();

  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const img = new Image();
      img.onload = () => {
        let width = img.width;
        let height = img.height;

        // Calcular nuevas dimensiones manteniendo el aspect ratio
        if (width > height) {
          if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
          }
        }

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = width;
        canvas.height = height;

        ctx.drawImage(img, 0, 0, width, height);

        // Convertir el canvas a Blob
        canvas.toBlob((blob) => {
          if (blob) {
            const endTime = performance.now();
            console.log(`Miniatura de imagen generada en ${(endTime - startTime).toFixed(2)} ms`);
            resolve({
              processedBlob: blob,
              processingTime: (endTime - startTime),
              originalSize: imageFileBlob.size,
              processedSize: blob.size
            });
          } else {
            reject(new Error('Fallo al generar el Blob de la miniatura.'));
          }
        }, imageFileBlob.type === 'image/png' ? 'image/png' : 'image/jpeg', quality); // Usa PNG si el original es PNG, sino JPEG por defecto
      };
      img.onerror = (error) => {
        reject(new Error('No se pudo cargar la imagen para procesamiento.'));
      };
      img.src = event.target.result;
    };
    reader.onerror = (error) => {
      reject(new Error('No se pudo leer el archivo de imagen.'));
    };
    reader.readAsDataURL(imageFileBlob);
  });
}