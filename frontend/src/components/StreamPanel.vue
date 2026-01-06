<script setup lang="ts">
import { computed } from 'vue'
import Tag from 'primevue/tag'
import type { CameraOption, StreamDefinition } from '../scripts/dashboardData'
import { getStreamUrl } from '../scripts/api'

const props = defineProps<{ camera: CameraOption; stream: StreamDefinition }>()
const cameraLabel = () => props.camera.displayName
const streamUrl = computed(() => getStreamUrl(props.camera.id, props.stream.id))
</script>

<template>
  <div class="stream-card">
    <!-- Stream as full background -->
    <img
      :src="streamUrl"
      alt="MJPEG stream"
      class="stream-bg"
    />

    <!-- Dark overlay for better text readability -->
    <div class="stream-overlay-bg"></div>

    <!-- Overlay content -->
    <div class="stream-overlay">
      <div class="stream-title">
        <div>
          <h3>{{ stream.title }}</h3>
          <p>{{ stream.description }}</p>
        </div>
        <Tag value="Live" severity="success" />
      </div>
      <span class="camera-label">{{ cameraLabel() }}</span>
    </div>
  </div>
</template>

<style scoped>
.stream-card {
  position: relative;
  width: 500px;
  height: 500px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stream-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Stream fills the card entirely */
.stream-bg {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  background: #000;
}

/* Gradient overlay for text readability */
.stream-overlay-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.5) 0%,
    rgba(0, 0, 0, 0) 50%,
    rgba(0, 0, 0, 0.6) 100%
  );
  pointer-events: none;
}

/* Overlay sits on top */
.stream-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: white;
  z-index: 1;
}

.stream-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
}

.stream-title h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
}

.stream-title p {
  margin: 0;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
}

.camera-label {
  font-weight: 600;
  font-size: 0.9rem;
  align-self: flex-end;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
  background: rgba(0, 0, 0, 0.3);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  backdrop-filter: blur(4px);
}
</style>
