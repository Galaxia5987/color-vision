<script setup lang="ts">
import { ref } from 'vue'
import Divider from 'primevue/divider'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Panel from 'primevue/panel'
import Slider from 'primevue/slider'
import type { CameraOption } from '../scripts/dashboardData'
import { processingModes } from '../scripts/dashboardData'

defineProps<{ camera?: CameraOption }>()

const processingMode = ref(processingModes[0]?.value ?? 'hsv')
const exposure = ref(100)
const hueRange = ref<[number, number]>([0, 360])
const saturationRange = ref<[number, number]>([0, 100])
const valueRange = ref<[number, number]>([0, 100])
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
</style>
