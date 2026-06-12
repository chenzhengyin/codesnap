<script setup lang="ts">
import { computed } from 'vue';
import { themes, languages, type ThemeKey } from '../themes';
import ProBadge from './ProBadge.vue';

const props = defineProps<{
  currentTheme: ThemeKey;
  padding: number;
  borderRadius: number;
  fontSize: number;
  language: string;
  isExporting: boolean;
  isPro: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:currentTheme', value: ThemeKey): void;
  (e: 'update:padding', value: number): void;
  (e: 'update:borderRadius', value: number): void;
  (e: 'update:fontSize', value: number): void;
  (e: 'update:language', value: string): void;
  (e: 'export', scale: number): void;
  (e: 'showModal'): void;
  (e: 'uploadBg', file: File): void;
  (e: 'uploadLogo', file: File): void;
  (e: 'clearBg'): void;
  (e: 'clearLogo'): void;
}>();

const themeList = computed(() =>
  Object.entries(themes).map(([key, val]) => ({
    key: key as ThemeKey,
    name: val.name,
    tier: val.tier,
  }))
);

function handleThemeChange(key: ThemeKey) {
  const theme = themes[key];
  if (theme.tier === 'pro' && !props.isPro) {
    emit('showModal');
    return;
  }
  emit('update:currentTheme', key);
}

function onFileChange(event: Event, type: 'bg' | 'logo') {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) {
    if (type === 'bg') {
      emit('uploadBg', file);
    } else {
      emit('uploadLogo', file);
    }
  }
  input.value = '';
}
</script>

<template>
  <div class="settings-panel">
    <div class="settings-group theme-group">
      <label>
        Theme
        <ProBadge v-if="!isPro" locked />
      </label>
      <select :value="currentTheme" @change="handleThemeChange(($event.target as HTMLSelectElement).value as ThemeKey)">
        <option v-for="t in themeList" :key="t.key" :value="t.key">
          {{ t.name }} {{ t.tier === 'pro' && !isPro ? '🔒' : '' }}
        </option>
      </select>
      <div v-if="!isPro" class="theme-hint">
        {{ themeList.filter(t => t.tier === 'free').length }} free — unlock 45+ more with Pro
      </div>
    </div>

    <div class="settings-group">
      <label>Language</label>
      <select
        :value="language"
        @change="emit('update:language', ($event.target as HTMLSelectElement).value)"
      >
        <option v-for="lang in languages" :key="lang.key" :value="lang.key">
          {{ lang.name }}
        </option>
      </select>
    </div>

    <div class="settings-group">
      <label>Padding <span>{{ padding }}px</span></label>
      <input
        type="range"
        min="16"
        max="64"
        :value="padding"
        @input="emit('update:padding', Number(($event.target as HTMLInputElement).value))"
      />
    </div>

    <div class="settings-group">
      <label>Border Radius <span>{{ borderRadius }}px</span></label>
      <input
        type="range"
        min="4"
        max="24"
        :value="borderRadius"
        @input="emit('update:borderRadius', Number(($event.target as HTMLInputElement).value))"
      />
    </div>

    <div class="settings-group">
      <label>Font Size <span>{{ fontSize }}px</span></label>
      <input
        type="range"
        min="12"
        max="24"
        :value="fontSize"
        @input="emit('update:fontSize', Number(($event.target as HTMLInputElement).value))"
      />
    </div>

    <div v-if="isPro" class="settings-group upload-group">
      <label>Custom Background</label>
      <div class="upload-row">
        <label class="file-btn">
          <input type="file" accept="image/*" @change="onFileChange($event, 'bg')" />
          Upload
        </label>
        <button class="clear-btn" @click="emit('clearBg')">Clear</button>
      </div>
    </div>

    <div v-if="isPro" class="settings-group upload-group">
      <label>Custom Logo</label>
      <div class="upload-row">
        <label class="file-btn">
          <input type="file" accept="image/*" @change="onFileChange($event, 'logo')" />
          Upload
        </label>
        <button class="clear-btn" @click="emit('clearLogo')">Clear</button>
      </div>
    </div>

    <div class="settings-group export-group">
      <label>
        Export PNG
        <span v-if="!isPro" class="watermark-hint">+ watermark</span>
        <ProBadge v-else />
      </label>
      <div class="export-buttons">
        <button @click="emit('export', 1)" :disabled="isExporting">1x</button>
        <button @click="emit('export', 2)" :disabled="isExporting">2x</button>
        <button @click="emit('export', 4)" :disabled="isExporting">4x</button>
      </div>
    </div>

    <div v-if="!isPro" class="settings-group upgrade-group">
      <button class="upgrade-link" @click="emit('showModal')">
        Unlock Pro — $5
      </button>
    </div>
  </div>
</template>

<style scoped>
.settings-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 20px 28px;
  padding: 20px 24px;
  background: #1a1b22;
  border-top: 1px solid #2e303a;
  align-items: flex-end;
}

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 140px;
}

.settings-group label {
  font-size: 12px;
  font-weight: 500;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.settings-group label span {
  color: #d1d5db;
  font-weight: 400;
  text-transform: none;
}

.watermark-hint {
  font-size: 10px;
  color: #6b7280;
  text-transform: none;
}

.settings-group select,
.settings-group input[type="range"] {
  background: #252631;
  border: 1px solid #2e303a;
  border-radius: 6px;
  color: #d1d5db;
  padding: 6px 10px;
  font-size: 13px;
  outline: none;
  cursor: pointer;
}

.settings-group select:focus {
  border-color: #aa3bff;
}

.settings-group input[type="range"] {
  padding: 0;
  height: 4px;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
}

.settings-group input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #aa3bff;
  cursor: pointer;
}

.theme-hint {
  font-size: 11px;
  color: #6b7280;
}

.upload-row {
  display: flex;
  gap: 8px;
}

.file-btn {
  position: relative;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #2e303a;
  background: #252631;
  color: #d1d5db;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.file-btn:hover {
  border-color: #aa3bff;
}

.file-btn input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.clear-btn {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #2e303a;
  background: transparent;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
}

.clear-btn:hover {
  color: #ef4444;
  border-color: #ef4444;
}

.export-group {
  margin-left: auto;
}

.export-buttons {
  display: flex;
  gap: 8px;
}

.export-buttons button {
  padding: 6px 14px;
  border-radius: 6px;
  border: 1px solid #2e303a;
  background: #252631;
  color: #d1d5db;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.export-buttons button:hover:not(:disabled) {
  background: #aa3bff;
  border-color: #aa3bff;
  color: #fff;
}

.export-buttons button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.upgrade-group {
  min-width: auto;
}

.upgrade-link {
  padding: 6px 14px;
  border-radius: 6px;
  border: none;
  background: linear-gradient(135deg, #aa3bff, #f59e0b);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.upgrade-link:hover {
  opacity: 0.9;
}

@media (max-width: 900px) {
  .export-group {
    margin-left: 0;
  }
}
</style>
