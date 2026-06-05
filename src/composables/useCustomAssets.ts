import { ref, onMounted } from 'vue';

const BG_KEY = 'codesnap_bg';
const LOGO_KEY = 'codesnap_logo';
const MAX_SIZE = 2 * 1024 * 1024; // 2MB

export function useCustomAssets() {
  const backgroundImage = ref<string>('');
  const logoImage = ref<string>('');

  onMounted(() => {
    backgroundImage.value = localStorage.getItem(BG_KEY) || '';
    logoImage.value = localStorage.getItem(LOGO_KEY) || '';
  });

  function handleFileUpload(file: File, type: 'bg' | 'logo') {
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file.');
      return;
    }
    if (file.size > MAX_SIZE) {
      alert('Image must be smaller than 2MB.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const base64 = e.target?.result as string;
      if (type === 'bg') {
        backgroundImage.value = base64;
        localStorage.setItem(BG_KEY, base64);
      } else {
        logoImage.value = base64;
        localStorage.setItem(LOGO_KEY, base64);
      }
    };
    reader.readAsDataURL(file);
  }

  function clearAsset(type: 'bg' | 'logo') {
    if (type === 'bg') {
      backgroundImage.value = '';
      localStorage.removeItem(BG_KEY);
    } else {
      logoImage.value = '';
      localStorage.removeItem(LOGO_KEY);
    }
  }

  return {
    backgroundImage,
    logoImage,
    handleFileUpload,
    clearAsset,
  };
}
