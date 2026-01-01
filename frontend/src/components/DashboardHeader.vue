<script setup lang="ts">
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import type { CameraOption } from '../scripts/dashboardData'
import { statusSeverityMap } from '../scripts/dashboardData'

defineProps<{ activeCamera?: CameraOption }>()
</script>

<template>
  <header class="header">
    <div>
      <p class="eyebrow">Galaxia Color Vision</p>
      <h1>Vision Dashboard</h1>
      <div class="meta">
        <span v-if="activeCamera" class="meta-label">Active camera:</span>
        <span v-if="activeCamera" class="meta-value">{{ activeCamera.id }}</span>
        <Tag
          v-if="activeCamera"
          :value="activeCamera.status"
          :severity="statusSeverityMap[activeCamera.status]"
          class="status-tag"
        />
      </div>
    </div>
    <div class="header-actions">
      <Button label="Add Camera" severity="primary" outlined />
    </div>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--muted);
  margin: 0 0 0.35rem 0;
}

h1 {
  margin: 0;
  font-size: clamp(1.8rem, 3vw, 2.6rem);
}

.meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.6rem;
  flex-wrap: wrap;
}

.meta-label {
  color: var(--muted);
  font-size: 0.9rem;
}

.meta-value {
  font-weight: 600;
}

.status-tag {
  text-transform: capitalize;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
</style>
