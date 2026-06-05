<script setup lang="ts">
import { ref } from 'vue';
import CodeEditor from './components/CodeEditor.vue';
import PreviewCard from './components/PreviewCard.vue';
import SettingsPanel from './components/SettingsPanel.vue';
import UpgradeBanner from './components/UpgradeBanner.vue';
import { useCodeEditor } from './composables/useCodeEditor';
import { useSettings } from './composables/useSettings';
import { useExport } from './composables/useExport';
import { usePro } from './composables/usePro';
import { useCustomAssets } from './composables/useCustomAssets';

const { code } = useCodeEditor();
const {
  currentTheme,
  padding,
  borderRadius,
  fontSize,
  language,
} = useSettings();
const { isExporting, exportPNG } = useExport();
const { isPro, openCheckout } = usePro();
const { backgroundImage, logoImage, handleFileUpload, clearAsset } = useCustomAssets();

const previewCardRef = ref<InstanceType<typeof PreviewCard> | null>(null);

async function handleExport(scale: number) {
  const card = previewCardRef.value?.cardRef;
  if (card) {
    await exportPNG(card, scale, { isPro: isPro.value });
  }
}
</script>

<template>
  <div class="app-container">
    <UpgradeBanner v-if="!isPro" @upgrade="openCheckout" />

    <header class="app-header">
      <h1>
        Code Screenshot
        <span v-if="isPro" class="pro-badge">Pro</span>
      </h1>
      <p>Create beautiful code snippets</p>
    </header>

    <main class="app-main">
      <div class="editor-pane">
        <CodeEditor v-model="code" />
      </div>
      <div class="preview-pane">
        <PreviewCard
          ref="previewCardRef"
          :code="code"
          :theme="currentTheme"
          :language="language"
          :padding="padding"
          :border-radius="borderRadius"
          :font-size="fontSize"
          :background-image="backgroundImage"
          :logo-image="logoImage"
        />
      </div>
    </main>

    <SettingsPanel
      v-model:current-theme="currentTheme"
      v-model:padding="padding"
      v-model:border-radius="borderRadius"
      v-model:font-size="fontSize"
      v-model:language="language"
      :is-exporting="isExporting"
      :is-pro="isPro"
      @export="handleExport"
      @upgrade="openCheckout"
      @upload-bg="handleFileUpload($event, 'bg')"
      @upload-logo="handleFileUpload($event, 'logo')"
      @clear-bg="clearAsset('bg')"
      @clear-logo="clearAsset('logo')"
    />
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.app-header {
  padding: 24px 0 16px;
  text-align: center;
}

.app-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #f3f4f6;
  margin: 0 0 4px;
  letter-spacing: -0.5px;
}

.app-header p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.pro-badge {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
  background: #aa3bff;
  border-radius: 4px;
  vertical-align: middle;
  letter-spacing: 0;
}

.app-main {
  display: flex;
  gap: 24px;
  flex: 1;
  min-height: 0;
  padding-bottom: 24px;
}

.editor-pane,
.preview-pane {
  flex: 1;
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

@media (max-width: 900px) {
  .app-main {
    flex-direction: column;
  }

  .editor-pane,
  .preview-pane {
    flex: none;
    height: 400px;
  }
}
</style>
