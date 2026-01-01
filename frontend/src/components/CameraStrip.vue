<script setup lang="ts">
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import type { CameraOption } from '../scripts/dashboardData'
import { statusSeverityMap } from '../scripts/dashboardData'

const props = defineProps<{ cameras: CameraOption[]; activeCameraId: string }>()
const emit = defineEmits<{ 'update:activeCameraId': [string] }>()

const setActive = (cameraId: string) => {
  if (cameraId !== props.activeCameraId) {
    emit('update:activeCameraId', cameraId)
  }
}
</script>

<template>
  <section class="camera-strip">
    <Card
      v-for="camera in cameras"
      :key="camera.id"
      class="camera-card"
      :class="{ active: camera.id === activeCameraId }"
      @click="setActive(camera.id)"
    >
      <template #title>
        <div class="camera-title">
          <span>{{ camera.id }}</span>
          <Tag :value="camera.status" :severity="statusSeverityMap[camera.status]" />
        </div>
      </template>
      <template #content>
        <div class="camera-meta">
          <span>ID {{ camera.id }}</span>
        </div>
      </template>
    </Card>
  </section>
</template>

<style scoped>
.camera-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 1rem;
}

.camera-card {
  cursor: pointer;
  border: 1px solid var(--border);
  background: var(--card);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.camera-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(25, 20, 12, 0.08);
}

.camera-card.active {
  border-color: var(--accent);
  box-shadow: inset 0 0 0 1px var(--accent);
}

.camera-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.camera-location {
  margin: 0 0 0.65rem 0;
  color: var(--muted);
}

.camera-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: var(--muted);
}
</style>
