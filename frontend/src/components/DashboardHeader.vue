<script setup lang="ts">
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import type { CameraOption } from '../scripts/dashboardData'
import { statusSeverityMap } from '../scripts/dashboardData'
import { ref } from 'vue';
import { addCamera, listDevices } from '@/scripts/api'

defineProps<{ activeCamera?: CameraOption }>()
const showDialog = ref<boolean>(false)
const devices = ref<string[]>([])
const loading = ref<boolean>(false)
const selectedDevice = ref<string | null>(null)
const aliasInput = ref<string>('')

async function openDialog() {
  showDialog.value = true
  loading.value = true
  devices.value = []
  selectedDevice.value = null
  aliasInput.value = ''
  try {
    devices.value = await listDevices()
  } catch {
    devices.value = []
  } finally {
    loading.value = false
  }
}

async function confirmSelection() {
  if (selectedDevice.value) {
    showDialog.value = false
    const status = await addCamera(selectedDevice.value, aliasInput.value)
    if(status != "\"OK\""){
      alert(`Failed to add camera! ${status}`)
      return
    }
    window.dispatchEvent(new CustomEvent('reload-cameras'))
  }
}
</script>

<template>
  <header class="header">
    <div>
      <p class="eyebrow">Galaxia Color Vision</p>
      <h1>Vision Dashboard</h1>
      <div class="meta">
        <span v-if="activeCamera" class="meta-label">Active camera:</span>
        <span v-if="activeCamera" class="meta-value">{{ activeCamera.displayName }}</span>
        <Tag
          v-if="activeCamera"
          :value="activeCamera.status"
          :severity="statusSeverityMap[activeCamera.status]"
          class="status-tag"
        />
      </div>
    </div>
    <div class="header-actions">
      <Button label="Add Camera" severity="primary" outlined @click="openDialog" />
      <Dialog header="Devices" v-model:visible="showDialog" modal :closable="true">
        <template #footer>
          <Button label="Close" text @click="showDialog = false" />
          <Button label="Okay" severity="primary" @click="confirmSelection" :disabled="!selectedDevice" />
        </template>

        <div style="min-width: 320px;">
          <p v-if="loading">Loading devices…</p>
          <p v-else-if="devices && devices.length === 0">No devices found.</p>
          <div v-else>
            <p>Please choose a camera:</p>
            <Dropdown
              v-model="selectedDevice"
              :options="devices"
              placeholder="Select a device"
              optionLabel=""
              style="width: 100%;"
            />
            <div style="margin-top: 1rem;">
              <label for="camera-alias" style="display: block; font-weight: 600; margin-bottom: 0.35rem;">
                Alias (optional)
              </label>
              <InputText id="camera-alias" v-model="aliasInput" placeholder="e.g. Front Dock" style="width: 100%;" />
            </div>
          </div>
        </div>
      </Dialog>
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
