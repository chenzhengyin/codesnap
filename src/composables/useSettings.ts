import { ref, watch } from 'vue';
import { themes, type ThemeKey } from '../themes';

export function useSettings() {
  const currentTheme = ref<ThemeKey>('dracula');
  const padding = ref(32);
  const borderRadius = ref(12);
  const fontSize = ref(14);
  const language = ref('javascript');

  watch(currentTheme, (theme) => {
    const existing = document.getElementById('hljs-theme') as HTMLLinkElement | null;
    const themeUrl = themes[theme].url;

    if (existing) {
      existing.href = themeUrl;
    } else {
      const link = document.createElement('link');
      link.id = 'hljs-theme';
      link.rel = 'stylesheet';
      link.href = themeUrl;
      document.head.appendChild(link);
    }
  }, { immediate: true });

  return {
    currentTheme,
    padding,
    borderRadius,
    fontSize,
    language,
    themeList: Object.entries(themes).map(([key, value]) => ({
      key: key as ThemeKey,
      name: value.name,
    })),
  };
}
