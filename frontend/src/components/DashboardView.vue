<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import DashboardHeader from './DashboardHeader.vue'
import CameraStrip from './CameraStrip.vue'
import StreamGrid from './StreamGrid.vue'
import ConfigPanel from './ConfigPanel.vue'
import DangerZone from './DangerZone.vue'
import { cameraOptions, streamDefinitions } from '../scripts/dashboardData'
import { listCameras } from '../scripts/api'
import type { CameraConfig } from '../scripts/api'
import type { CameraOption } from '../scripts/dashboardData'

const cameras = ref<CameraOption[]>(cameraOptions)
const cameraConfigs = ref<CameraConfig[]>([])
const activeCameraId = ref(cameras.value[0]?.id ?? '')

const activeCamera = computed(() => {
  return cameras.value.find((camera) => camera.id === activeCameraId.value) ?? cameras.value[0]
})

const activeCameraConfig = computed(() => {
  return cameraConfigs.value.find((camera) => camera.name === activeCameraId.value) ?? null
})

const refreshCameras = async () => {
  try {
    const data = await listCameras()
    cameraConfigs.value = data.cameras
    cameras.value = data.cameras.map((camera) => ({
      id: camera.name,
      status: 'online',
    }))
    if (!cameras.value.find((camera) => camera.id === activeCameraId.value)) {
      activeCameraId.value = cameras.value[0]?.id ?? ''
    }
  } catch {
    cameras.value = cameraOptions
  }
}

const handleConfigUpdated = (updated: CameraConfig) => {
  const index = cameraConfigs.value.findIndex((camera) => camera.name === updated.name)
  if (index >= 0) {
    cameraConfigs.value[index] = updated
  } else {
    cameraConfigs.value.push(updated)
  }
}

onMounted(() => {
  void refreshCameras()
})

onMounted(() => {
  const onReload = () => {
    void refreshCameras()
  }
  window.addEventListener('reload-cameras', onReload)
})
</script>

<template>
  <div class="dashboard">
    <DashboardHeader :active-camera="activeCamera" />
    <CameraStrip v-model:active-camera-id="activeCameraId" :cameras="cameras" />
    <div class="dashboard-body">
      <StreamGrid v-if="activeCamera" :camera="activeCamera" :streams="streamDefinitions" />
      <aside class="sidebar">
        <ConfigPanel
          v-if="activeCamera"
          :camera="activeCamera"
          :camera-config="activeCameraConfig"
          @updated="handleConfigUpdated"
        />
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
