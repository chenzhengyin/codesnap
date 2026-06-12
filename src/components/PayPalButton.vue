<script setup lang="ts">
import { onMounted } from 'vue';

declare global {
  interface Window {
    paypal: {
      HostedButtons: (config: {
        hostedButtonId: string;
        onApprove?: (data: unknown) => void;
      }) => {
        render: (selector: string) => void;
      };
    };
  }
}

const props = defineProps<{
  containerId: string;
}>();

const emit = defineEmits<{
  (e: 'success'): void;
}>();

onMounted(() => {
  if (!window.paypal || !window.paypal.HostedButtons) {
    console.error('PayPal SDK not loaded');
    return;
  }

  window.paypal.HostedButtons({
    hostedButtonId: '862XKGDFQTG8C',
    onApprove: () => {
      emit('success');
    },
  }).render(`#${props.containerId}`);
});
</script>

<template>
  <div :id="containerId" ref="containerRef" class="paypal-container"></div>
</template>

<style scoped>
.paypal-container {
  min-width: 150px;
}
</style>
