<script setup lang="ts">
  import Card from 'primevue/card'
import Tag from 'primevue/tag'
import type { CameraOption, StreamDefinition } from '../scripts/dashboardData'

const props = defineProps<{ camera: CameraOption; stream: StreamDefinition }>()

const cameraLabel = () => props.camera.id
</script>

<template>
  <Card class="stream-card">
    <template #title>
      <div class="stream-title">
        <div>
          <h3>{{ stream.title }}</h3>
          <p>{{ stream.description }}</p>
        </div>
        <Tag value="Live" severity="success" />
      </div>
    </template>

    <template #content>
      <div class="stream-frame">
        <div class="stream-overlay">
          <span>{{ cameraLabel() }}</span>
        </div>

        <div style="width:100%; margin-top:0.75rem;">
          <img
            :src="`/streams/${camera.id}/${stream.id}`"
            style="width:100%; height:100%; border-radius:8px; object-fit:cover;"
            alt="MJPEG stream"
            aria-label="MJPEG stream"
          />
        </div>
      </div>
    </template>
  </Card>
</template>

<style scoped>
.stream-card {
  border: 1px solid var(--border);
  background: var(--panel);
}

.stream-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.stream-title h3 {
  margin: 0 0 0.15rem 0;
}

.stream-title p {
  margin: 0;
  color: var(--muted);
}

.stream-controls {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 1rem;
}

.stream-frame {
  border-radius: 12px;
  border: 1px dashed var(--border-strong);
  background:
    linear-gradient(140deg, rgba(12, 75, 55, 0.18), rgba(17, 120, 79, 0.08)),
    repeating-linear-gradient(45deg, rgba(15, 15, 15, 0.05), rgba(15, 15, 15, 0.05) 10px, transparent 10px, transparent 20px);
  min-height: 220px;
  display: flex;
  align-items: flex-end;
  padding: 1rem;
  color: var(--accent-strong);
}

.stream-overlay {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-weight: 600;
  font-size: 0.9rem;
}

@media (max-width: 640px) {
  .stream-frame {
    min-height: 180px;
  }
}
</style>
