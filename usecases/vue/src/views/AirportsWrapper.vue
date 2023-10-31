<script setup lang="ts">
import AriportsMap from '../components/AirportsMap.vue'
import DeparturesCount from '../components/DeparturesCount.vue'
</script>

<template>
  <div class="airports-wrapper">
    <div class="airports-item">
      <AriportsMap />
    </div>
    <div class="airports-item">
      <DeparturesCount />
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .airports-wrapper {
    height: 100%; 
    width: 100%;
    display: flex;
    gap: 16px
  }
  .airports-item {
    flex: 1;
  }
}
</style>
