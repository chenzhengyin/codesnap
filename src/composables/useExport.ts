import { ref } from 'vue';
import html2canvas from 'html2canvas';

const WATERMARK_TEXT = 'Made by CodeSnap';

function drawWatermark(canvas: HTMLCanvasElement, text: string) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  ctx.save();
  ctx.globalAlpha = 0.15;

  const fontSize = Math.max(16, Math.floor(canvas.width * 0.025));
  ctx.font = `bold ${fontSize}px system-ui, -apple-system, sans-serif`;
  ctx.fillStyle = '#ffffff';
  ctx.textAlign = 'right';
  ctx.textBaseline = 'bottom';

  const padding = Math.max(16, Math.floor(canvas.width * 0.02));
  ctx.fillText(text, canvas.width - padding, canvas.height - padding);

  ctx.restore();
}

export function useExport() {
  const isExporting = ref(false);

  async function exportPNG(
    element: HTMLElement,
    scale: number = 2,
    options: { isPro?: boolean } = {}
  ): Promise<void> {
    if (!element) return;

    isExporting.value = true;
    try {
      const canvas = await html2canvas(element, {
        scale,
        backgroundColor: null,
        logging: false,
        useCORS: true,
        allowTaint: true,
      });

      if (!options.isPro) {
        drawWatermark(canvas, WATERMARK_TEXT);
      }

      const link = document.createElement('a');
      link.download = `code-screenshot@${scale}x.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    } finally {
      isExporting.value = false;
    }
  }

  return {
    isExporting,
    exportPNG,
  };
}
