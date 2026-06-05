import { ref, computed } from 'vue';

const defaultCode = `function greet(name) {
  const message = \`Hello, \${name}!\`;
  console.log(message);
  return message;
}

greet('World');`;

export function useCodeEditor() {
  const code = ref(defaultCode);

  const lineCount = computed(() => code.value.split('\n').length);

  const lineNumbers = computed(() => {
    return Array.from({ length: lineCount.value }, (_, i) => i + 1);
  });

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
          code.value = before.substring(0, lineStart) + currentLine.substring(2) + after;
          target.selectionStart = target.selectionEnd = start - 2;
        } else if (currentLine.startsWith(' ')) {
          code.value = before.substring(0, lineStart) + currentLine.substring(1) + after;
          target.selectionStart = target.selectionEnd = start - 1;
        }
      } else {
        code.value = code.value.substring(0, start) + spaces + code.value.substring(end);
        target.selectionStart = target.selectionEnd = start + spaces.length;
      }
    }
  }

  return {
    code,
    lineCount,
    lineNumbers,
    handleKeydown,
  };
}
