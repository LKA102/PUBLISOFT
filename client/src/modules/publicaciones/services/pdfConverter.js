// src/modules/publicaciones/services/pdfConverter.js

// Importación desde CDN con alias para fontkit
async function loadModules() {
  const { PDFDocument, rgb } = await import('https://cdn.skypack.dev/pdf-lib');
  const fontkit = await import('https://cdn.skypack.dev/@pdf-lib/fontkit');
  return { PDFDocument, rgb, fontkit };
}

const {PDFDocument, rgb, fontkit} = loadModules();

// Función para convertir archivos a PDF
export const convertToPDF = async (file) => {
  if (file.type === 'application/pdf') {
    return file;
  }

  try {
    // Crear nuevo documento PDF
    const pdfDoc = await PDFDocument.create();

    // Registrar fontkit con el nombre correcto
    pdfDoc.registerFontkit(fontkit.default);

    const page = pdfDoc.addPage([550, 750]);

    // Agregar título
    page.drawText(`Documento convertido: ${file.name}`, {
      x: 50,
      y: 700,
      size: 18,
      color: rgb(0, 0.2, 0.4),
    });

    // Procesar imagen si es PNG/JPG
    if (file.type.startsWith('image/')) {
      try {
        const imageBytes = await file.arrayBuffer();
        let image;

        if (file.type === 'image/jpeg' || file.type === 'image/jpg') {
          image = await pdfDoc.embedJpg(imageBytes);
        } else if (file.type === 'image/png') {
          image = await pdfDoc.embedPng(imageBytes);
        }

        // Escalar imagen para que quepa
        const scale = Math.min(450 / image.width, 600 / image.height);
        const width = image.width * scale;
        const height = image.height * scale;

        page.drawImage(image, {
          x: 50,
          y: 700 - height - 20, // 20px debajo del título
          width,
          height,
        });
      } catch (imgError) {
        console.error('Error procesando imagen:', imgError);
        page.drawText('(Imagen no procesada)', {
          x: 50,
          y: 650,
          size: 12,
          color: rgb(0.8, 0, 0),
        });
      }
    }

    const pdfBytes = await pdfDoc.save();
    return new Blob([pdfBytes], { type: 'application/pdf' });

  } catch (error) {
    console.error('Error en convertToPDF:', error);
    throw new Error(`Error al convertir a PDF: ${error.message}`);
  }
};

// Función para generar miniaturas
export const generateThumbnail = async (pdfBlob) => {
  const canvas = document.createElement('canvas');
  canvas.width = 200;
  canvas.height = 280;
  const ctx = canvas.getContext('2d');

  // Fondo
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Icono de documento
  ctx.fillStyle = '#1976D2';
  ctx.font = 'bold 24px Arial';
  ctx.fillText('PDF', 80, 150);

  // Texto
  ctx.fillStyle = '#333';
  ctx.font = '12px Arial';
  ctx.fillText('Vista previa', 70, 180);

  return canvas.toDataURL('image/jpeg');
};

// Exportación para CommonJS (por si acaso)
export default {
  convertToPDF,
  generateThumbnail
};
