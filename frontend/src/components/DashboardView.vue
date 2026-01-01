<script setup lang="ts">
import { computed, ref } from 'vue'
import DashboardHeader from './DashboardHeader.vue'
import CameraStrip from './CameraStrip.vue'
import StreamGrid from './StreamGrid.vue'
import ConfigPanel from './ConfigPanel.vue'
import DangerZone from './DangerZone.vue'
import { cameraOptions, streamDefinitions } from '../scripts/dashboardData'

const activeCameraId = ref(cameraOptions[0]?.id ?? '')

const activeCamera = computed(() => {
  return cameraOptions.find((camera) => camera.id === activeCameraId.value) ?? cameraOptions[0]
})
</script>

<template>
  <div class="dashboard">
    <DashboardHeader :active-camera="activeCamera" />
    <CameraStrip v-model:active-camera-id="activeCameraId" :cameras="cameraOptions" />
    <div class="dashboard-body">
      <StreamGrid :camera="activeCamera" :streams="streamDefinitions" />
      <aside class="sidebar">
        <ConfigPanel :camera="activeCamera" />
        <DangerZone />
      </aside>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 2.5rem clamp(1.5rem, 4vw, 3.5rem) 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dashboard-body {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: minmax(0, 2.1fr) minmax(280px, 1fr);
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

@media (max-width: 980px) {
  .dashboard-body {
    grid-template-columns: 1fr;
  }
}
</style>
