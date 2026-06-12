import { ref } from 'vue';
import html2canvas from 'html2canvas';

export function useExport() {
  const isExporting = ref(false);

  async function exportPNG(
    element: HTMLElement,
    scale: number = 2,
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
