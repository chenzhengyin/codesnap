<script setup lang="ts">
const emit = defineEmits<{
  (e: 'upgrade'): void;
}>();
</script>

<template>
  <div class="upgrade-banner">
    <div class="banner-content">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
      </svg>
      <span>
        <strong>Upgrade to Pro</strong> — Remove watermark, unlock 50+ themes, and add custom backgrounds.
      </span>
    </div>
    <button class="upgrade-btn" @click="emit('upgrade')">
      Upgrade
    </button>
  </div>
</template>

<style scoped>
.upgrade-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 20px;
  margin-bottom: 16px;
  background: linear-gradient(90deg, rgba(170, 59, 255, 0.15), rgba(251, 191, 36, 0.08));
  border: 1px solid rgba(170, 59, 255, 0.3);
  border-radius: 10px;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #d1d5db;
}

.banner-content strong {
  color: #fbbf24;
  font-weight: 600;
}

.upgrade-btn {
  padding: 6px 16px;
  border-radius: 6px;
  border: none;
  background: #aa3bff;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
}

.upgrade-btn:hover {
  background: #9333ea;
}

@media (max-width: 600px) {
  .upgrade-banner {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .banner-content {
    justify-content: center;
  }
}
</style>
