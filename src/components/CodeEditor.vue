<script setup lang="ts">
import { computed, ref } from 'vue';

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const code = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
});

const lineCount = computed(() => code.value.split('\n').length);
const lineNumbers = computed(() =>
  Array.from({ length: lineCount.value }, (_, i) => i + 1)
);

function handleKeydown(event: KeyboardEvent) {
  const target = event.target as HTMLTextAreaElement;

  if (event.key === 'Tab') {
    event.preventDefault();
    const start = target.selectionStart;
    const end = target.selectionEnd;
    const spaces = '  ';

    if (event.shiftKey) {
      const before = code.value.substring(0, start);
      const after = code.value.substring(end);
      const lineStart = before.lastIndexOf('\n') + 1;
      const currentLine = before.substring(lineStart);
      if (currentLine.startsWith('  ')) {
        code.value =
          before.substring(0, lineStart) +
          currentLine.substring(2) +
          after;
        target.selectionStart = target.selectionEnd = start - 2;
      } else if (currentLine.startsWith(' ')) {
        code.value =
          before.substring(0, lineStart) +
          currentLine.substring(1) +
          after;
        target.selectionStart = target.selectionEnd = start - 1;
      }
    } else {
      code.value =
        code.value.substring(0, start) + spaces + code.value.substring(end);
      target.selectionStart = target.selectionEnd = start + spaces.length;
    }
  }
}

// Sync scroll
const lineNumbersRef = ref<HTMLDivElement | null>(null);
function handleScroll(e: Event) {
  const target = e.target as HTMLTextAreaElement;
  if (lineNumbersRef.value) {
    lineNumbersRef.value.scrollTop = target.scrollTop;
  }
}
</script>

<template>
  <div class="code-editor">
    <div class="editor-header">
      <span>Editor</span>
    </div>
    <div class="editor-body">
      <div class="line-numbers" ref="lineNumbersRef">
        <div v-for="n in lineNumbers" :key="n" class="line-number">
          {{ n }}
        </div>
      </div>
      <textarea
        ref="textareaRef"
        v-model="code"
        @keydown="handleKeydown"
        @scroll="handleScroll"
        spellcheck="false"
        autocapitalize="off"
        autocomplete="off"
        autocorrect="off"
      />
    </div>
  </div>
</template>

<style scoped>
.code-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #16171d;
  border-radius: 12px;
  border: 1px solid #2e303a;
  overflow: hidden;
}

.editor-header {
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 500;
  color: #9ca3af;
  border-bottom: 1px solid #2e303a;
  background: #1a1b22;
}

.editor-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.line-numbers {
  padding: 16px 12px 16px 16px;
  font-family: ui-monospace, Consolas, 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  background: #16171d;
  text-align: right;
  user-select: none;
  overflow: hidden;
}

.line-number {
  min-width: 28px;
}

textarea {
  flex: 1;
  padding: 16px;
  border: none;
  outline: none;
  resize: none;
  background: #16171d;
  color: #d1d5db;
  font-family: ui-monospace, Consolas, 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  tab-size: 2;
  white-space: pre;
  overflow: auto;
}

textarea::selection {
  background: rgba(170, 59, 255, 0.3);
}
</style>
