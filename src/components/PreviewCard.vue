<script setup lang="ts">
import { computed, ref, watch, nextTick } from 'vue';
import hljs from 'highlight.js';
import MacWindowFrame from './MacWindowFrame.vue';
import { themes, type ThemeKey } from '../themes';

const props = defineProps<{
  code: string;
  theme: ThemeKey;
  language: string;
  padding: number;
  borderRadius: number;
  fontSize: number;
  backgroundImage?: string;
  logoImage?: string;
  isPro?: boolean;
}>();

const cardRef = ref<HTMLDivElement | null>(null);
const highlightedCode = ref('');

const currentTheme = computed(() => themes[props.theme]);

const cardStyle = computed(() => ({
  borderRadius: `${props.borderRadius}px`,
  fontSize: `${props.fontSize}px`,
}));

const codeStyle = computed(() => ({
  padding: `${props.padding}px`,
  background: currentTheme.value.bg,
  color: currentTheme.value.fg,
}));

watch(
  () => [props.code, props.theme, props.language],
  async () => {
    await nextTick();
    try {
      const result = hljs.highlight(props.code, {
        language: props.language,
        ignoreIllegals: true,
      });
      highlightedCode.value = result.value;
    } catch {
      highlightedCode.value = hljs.highlightAuto(props.code).value;
    }
  },
  { immediate: true }
);

defineExpose({ cardRef });
</script>

<template>
  <div class="preview-wrapper">
    <div class="preview-label">Preview</div>
    <div ref="cardRef" class="preview-card" :style="cardStyle">
      <div v-if="backgroundImage" class="custom-bg" :style="{ backgroundImage: `url(${backgroundImage})` }"></div>
      <MacWindowFrame :theme="theme" :language="language" />
      <div class="code-content" :style="codeStyle">
        <pre><code class="hljs" v-html="highlightedCode"></code></pre>
      </div>
      <img v-if="logoImage" class="custom-logo" :src="logoImage" alt="logo" />
      <div v-if="!isPro" class="watermark">Made by CodeSnap</div>
    </div>
  </div>
</template>

<style scoped>
.preview-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.preview-label {
  font-size: 13px;
  font-weight: 500;
  color: #9ca3af;
  margin-bottom: 12px;
  padding-left: 4px;
}

.preview-card {
  position: relative;
  background: #1e1e2e;
  overflow: hidden;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.4),
    0 8px 20px rgba(0, 0, 0, 0.3);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.code-content {
  flex: 1;
  overflow: auto;
  min-height: 0;
}

.code-content pre {
  margin: 0;
}

.code-content code {
  font-family: ui-monospace, Consolas, 'Courier New', monospace;
  line-height: 1.6;
  display: block;
  background: transparent !important;
}

.code-content :deep(.hljs) {
  background: transparent !important;
}

.custom-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.custom-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
}

.custom-logo {
  position: absolute;
  bottom: 16px;
  right: 16px;
  max-width: 80px;
  max-height: 40px;
  object-fit: contain;
  z-index: 2;
  opacity: 0.85;
}

.watermark {
  position: absolute;
  bottom: 12px;
  right: 12px;
  padding: 5px 12px;
  background: rgba(255, 255, 255, 0.85);
  color: rgba(0, 0, 0, 0.85);
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 13px;
  font-weight: bold;
  border-radius: 6px;
  pointer-events: none;
  z-index: 3;
  letter-spacing: 0.3px;
  user-select: none;
}
</style>
