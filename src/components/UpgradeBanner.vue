<script setup lang="ts">
const emit = defineEmits<{
  showModal: [];
}>();
</script>

<template>
  <div class="upgrade-banner" @click="emit('showModal')">
    <div class="banner-content">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
      </svg>
      <span>Upgrade to Pro — Remove watermark, unlock 50+ themes, custom backgrounds. <strong>Click to upgrade</strong></span>
    </div>
  </div>
</template>

<style scoped>
.upgrade-banner {
  padding: 8px 16px;
  margin-bottom: 12px;
  background: linear-gradient(90deg, rgba(170, 59, 255, 0.12), rgba(251, 191, 36, 0.06));
  border: 1px solid rgba(170, 59, 255, 0.25);
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}

.upgrade-banner:hover {
  border-color: rgba(170, 59, 255, 0.5);
  background: linear-gradient(90deg, rgba(170, 59, 255, 0.18), rgba(251, 191, 36, 0.1));
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #9ca3af;
}

.banner-content strong {
  color: #fbbf24;
  font-weight: 500;
}

.banner-content span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 600px) {
  .banner-content span {
    white-space: normal;
  }
}
</style>
