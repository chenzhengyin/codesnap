<script setup lang="ts">
const props = defineProps<{
  locked?: boolean;
}>();
</script>

<template>
  <span class="pro-badge-small" :class="{ locked }">
    <svg v-if="locked" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
    Pro
  </span>
</template>

<style scoped>
.pro-badge-small {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 1px 6px;
  font-size: 10px;
  font-weight: 600;
  color: #fff;
  background: #aa3bff;
  border-radius: 4px;
  letter-spacing: 0.3px;
  flex-shrink: 0;
}

.pro-badge-small.locked {
  background: #4b5563;
  color: #9ca3af;
}

.pro-badge-small svg {
  stroke: currentColor;
}
</style>
