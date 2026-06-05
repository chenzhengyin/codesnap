<script setup lang="ts">
import { computed } from 'vue';
import type { ThemeKey } from '../themes';

const props = defineProps<{
  theme: ThemeKey;
  language?: string;
}>();

const isLight = computed(() => {
  return ['github-light', 'atom-one-light', 'solarized-light'].includes(props.theme);
});
</script>

<template>
  <div class="mac-window-frame" :class="{ light: isLight }">
    <div class="window-controls">
      <span class="dot red"></span>
      <span class="dot yellow"></span>
      <span class="dot green"></span>
    </div>
    <div class="window-title" v-if="language">
      {{ language }}
    </div>
    <div class="window-spacer"></div>
  </div>
</template>

<style scoped>
.mac-window-frame {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.03);
}

.mac-window-frame.light {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(0, 0, 0, 0.02);
}

.window-controls {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: block;
}

.red {
  background: #ff5f56;
}

.yellow {
  background: #ffbd2e;
}

.green {
  background: #27c93f;
}

.window-title {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  font-family: system-ui, sans-serif;
  text-transform: lowercase;
  flex-shrink: 0;
}

.mac-window-frame.light .window-title {
  color: rgba(0, 0, 0, 0.35);
}

.window-spacer {
  flex: 1;
}
</style>
