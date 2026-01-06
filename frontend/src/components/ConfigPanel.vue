<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import InputText from 'primevue/inputtext'
import Panel from 'primevue/panel'
import Slider from 'primevue/slider'
import type { CameraOption } from '../scripts/dashboardData'
import { processingModes } from '../scripts/dashboardData'
import { saveConfig, updateCameraSettings } from '../scripts/api'
import type { CameraConfig } from '../scripts/api'

const props = defineProps<{ camera?: CameraOption; cameraConfig?: CameraConfig | null }>()
const emit = defineEmits<{ updated: [CameraConfig] }>()

const processingMode = ref(processingModes[0]?.value ?? 'hsv')
const exposure = ref(100)
const hueRange = ref<[number, number]>([0, 360])
const saturationRange = ref<[number, number]>([0, 100])
const valueRange = ref<[number, number]>([0, 100])
const minArea = ref<number | null>(0)
const maxArea = ref<number | null>(0)
const enableRawFeed = ref<boolean>(false)
const enableTargetFeed = ref<boolean>(false)

const isUpdating = ref(false)
const isSaving = ref(false)
const statusMessage = ref('')
const statusTone = ref<'success' | 'error' | ''>('')

const canApply = computed(() => Boolean(props.camera && props.cameraConfig))

const toHueBackend = (value: number) => Math.round((value / 360) * 180)
const toSvBackend = (value: number) => Math.round((value / 100) * 255)
const fromHueBackend = (value: number) => Math.round((value / 180) * 360)
const fromSvBackend = (value: number) => Math.round((value / 255) * 100)

const setStatus = (message: string, tone: 'success' | 'error') => {
  statusMessage.value = message
  statusTone.value = tone
}

const clearStatus = () => {
  statusMessage.value = ''
  statusTone.value = ''
}

const applySettings = async () => {
  if (!props.camera || !props.cameraConfig || isUpdating.value) {
    return
  }

  isUpdating.value = true
  clearStatus()
  try {
    const lower = [
      toHueBackend(hueRange.value[0]),
      toSvBackend(saturationRange.value[0]),
      toSvBackend(valueRange.value[0]),
    ]
    const upper = [
      toHueBackend(hueRange.value[1]),
      toSvBackend(saturationRange.value[1]),
      toSvBackend(valueRange.value[1]),
    ]
    const update: CameraConfig = {
      ...props.cameraConfig,
      exposure: exposure.value,
      detection: {
        ...props.cameraConfig.detection,
        limits: [lower, upper],
        min_area: Math.max(0, Math.round(minArea.value ?? 0)),
        max_area: Math.max(0, Math.round(maxArea.value ?? 0)),
      },
      detection_stream_enabled: enableRawFeed.value, 
      mask_stream_enabled: enableTargetFeed.value,
    }
    const response = await updateCameraSettings(props.camera.id, update)
    emit('updated', response.camera)
    setStatus('Camera updated.', 'success')
  } catch {
    setStatus('Failed to update camera.', 'error')
  } finally {
    isUpdating.value = false
  }
}

const persistConfig = async () => {
  if (isSaving.value) {
    return
  }
  isSaving.value = true
  clearStatus()
  try {
    await saveConfig()
    setStatus('Config saved to disk.', 'success')
  } catch {
    setStatus('Failed to save config.', 'error')
  } finally {
    isSaving.value = false
  }
}

watch(
  () => props.cameraConfig,
  (config) => {
    if (!config) {
      return
    }
    exposure.value = config.exposure
    const [lower, upper] = config.detection.limits
    hueRange.value = [fromHueBackend(lower[0] ?? 0), fromHueBackend(upper[0] ?? 0)]
    saturationRange.value = [fromSvBackend(lower[1] ?? 0), fromSvBackend(upper[1] ?? 0)]
    valueRange.value = [fromSvBackend(lower[2] ?? 0), fromSvBackend(upper[2] ?? 0)]
    minArea.value = config.detection.min_area ?? 0
    maxArea.value = config.detection.max_area ?? 0
    enableRawFeed.value = config.detection_stream_enabled ?? false
    enableTargetFeed.value = config.detection_stream_enabled ?? false
    clearStatus()
  },
  { immediate: true }
)
</script>

<template>
  <Panel header="Configuration" toggleable>
    <div class="panel-body">
      <div class="field">
        <label class="label">Camera</label>
        <InputText :value="camera?.id ?? 'Not selected'" disabled />
      </div>
      <div class="field">
        <label class="label">Pipeline</label>
        <Dropdown v-model="processingMode" :options="processingModes" option-label="label" option-value="value" />
      </div>
      <Divider />
      <div class="field">
        <label class="label">Exposure</label>
        <div class="range-row">
          <Slider v-model="exposure" :min="0" :max="100" />
          <span class="value">{{ exposure }}%</span>
        </div>
      </div>
      <Divider />
      <div class="field">
        <label class="label">Hue</label>
        <div class="range-row">
          <Slider v-model="hueRange" :min="0" :max="360" :step="1" :range="true" />
          <span class="value">{{ hueRange[0] }}-{{ hueRange[1] }}</span>
        </div>
      </div>

      <div class="field">
        <label class="label">Saturation (%)</label>
        <div class="range-row">
          <Slider v-model="saturationRange" :min="0" :max="100" :step="1" :range="true" />
          <span class="value">{{ saturationRange[0] }}-{{ saturationRange[1] }}%</span>
        </div>
      </div>

      <div class="field">
        <label class="label">Value / Brightness (%)</label>
        <div class="range-row">
          <Slider v-model="valueRange" :min="0" :max="100" :step="1" :range="true" />
          <span class="value">{{ valueRange[0] }}-{{ valueRange[1] }}%</span>
        </div>
      </div>
      <Divider />
      <div class="field">
        <label class="label">Min Area</label>
        <InputNumber v-model="minArea" :min="0" :use-grouping="false" />
      </div>
      <div class="field">
        <label class="label">Max Area</label>
        <InputNumber v-model="maxArea" :min="0" :use-grouping="false" />
      </div>
      <Divider />
      <div class="field">
        <label class="label">Enable Raw Feed</label>
        <Checkbox v-model="enableRawFeed" :binary="true" />
      </div>
      <div class="field">
        <label class="label">Enable Processed Feed</label>
        <Checkbox v-model="enableTargetFeed" :binary="true" />
      </div>
      <Divider />
      <p v-if="statusMessage" class="status" :class="statusTone">{{ statusMessage }}</p>
      <div class="actions">
        <Button
          label="Apply"
          severity="primary"
          :loading="isUpdating"
          :disabled="!canApply"
          @click="applySettings"
        />
        <Button label="Save Config" outlined :loading="isSaving" @click="persistConfig" />
      </div>
    </div>
  </Panel>
</template>
<style scoped>
.panel-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.label {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--muted);
}

.range-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.75rem;
  align-items: center;
}

.value {
  font-weight: 600;
  color: var(--accent-strong);
}


.actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.status {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 600;
}

.status.success {
  color: #177a3d;
}

.status.error {
  color: #b22121;
}
</style>
