<script setup lang="ts">
import Button from 'primevue/button'
import Card from 'primevue/card'
import { dangerActions } from '../scripts/dashboardData'
</script>

<template>
  <Card class="danger-card">
    <template #title>
      <div class="danger-title">
        <span>Danger Zone</span>
      </div>
    </template>
    <template #content>
      <div class="danger-list">
        <div v-for="action in dangerActions" :key="action.id" class="danger-item">
          <div>
            <p class="danger-label">{{ action.label }}</p>
            <p class="danger-description">{{ action.description }}</p>
          </div>
          <Button label="Execute" severity="danger" outlined />
        </div>
      </div>
    </template>
  </Card>
</template>

<style scoped>
.danger-card {
  border: 1px solid rgba(170, 35, 35, 0.3);
}

.danger-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.danger-pill {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #7d1f1f;
}

.danger-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.danger-item {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
}

.danger-label {
  margin: 0 0 0.2rem 0;
  font-weight: 600;
}

.danger-description {
  margin: 0;
  font-size: 0.85rem;
}

@media (max-width: 620px) {
  .danger-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
