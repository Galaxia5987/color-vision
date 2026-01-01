<script setup lang="ts">
import StreamPanel from './StreamPanel.vue'
import type { CameraOption, StreamDefinition } from '../scripts/dashboardData'

defineProps<{ camera: CameraOption; streams: StreamDefinition[] }>()
</script>

<template>
  <div class="stream-grid">
    <StreamPanel v-for="stream in streams" :key="stream.id" :camera="camera" :stream="stream" />
  </div>
</template>

<style scoped>
.stream-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}
</style>
