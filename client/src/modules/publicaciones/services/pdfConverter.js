// src/modules/publicaciones/services/pdfConverter.js
import { PDFDocument, rgb } from 'pdf-lib';
import * as fontkit from '@pdf-lib/fontkit';

// Función para convertir archivos a PDF
export const convertToPDF = async (file) => {
  if (file.type === 'application/pdf') {
    return file;
  }

  try {
    const pdfDoc = await PDFDocument.create();
    pdfDoc.registerFontkit(fontkit);
    
    const page = pdfDoc.addPage([550, 750]);
    
    page.drawText(`Documento convertido: ${file.name}`, {
      x: 50,
      y: 700,
      size: 18,
      color: rgb(0, 0.2, 0.4),
    });

    if (file.type.startsWith('image/')) {
      const imageBytes = await file.arrayBuffer();
      let image;
      
      if (file.type === 'image/jpeg') {
        image = await pdfDoc.embedJpg(imageBytes);
      } else {
        image = await pdfDoc.embedPng(imageBytes);
      }
      
      page.drawImage(image, {
        x: 50,
        y: 500,
        width: image.width * 0.5,
        height: image.height * 0.5,
      });
    }
    
    const pdfBytes = await pdfDoc.save();
    return new Blob([pdfBytes], { type: 'application/pdf' });
  } catch (error) {
    console.error('Error al convertir a PDF:', error);
    throw new Error('No se pudo convertir el documento a PDF');
  }
};

// Función para generar miniaturas
export const generateThumbnail = async (pdfBlob) => {
  try {
    const canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 280;
    const ctx = canvas.getContext('2d');
    
    ctx.fillStyle = '#f5f5f5';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#1976D2';
    ctx.font = '80px Arial';
    ctx.fillText('📄', 60, 150);
    
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.fillText('Vista previa PDF', 50, 200);
    
    return canvas.toDataURL('image/jpeg');
  } catch (error) {
    console.error('Error generando miniatura:', error);
    return null;
  }
};

// Exportación por defecto para compatibilidad
export default {
  convertToPDF,
  generateThumbnail
};