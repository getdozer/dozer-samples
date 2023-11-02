<script setup lang="ts">
import { useDozerEvent, useDozerQuery } from '@dozerjs/dozer-vue';
const center = {
  lng: 50.993667602539063,
  lat: 50.7
};
const zoom = 4;
const { records, connect } = useDozerQuery('airports_count', { limit: 5000 });
const { stream } = useDozerEvent([{ endpoint: 'airports_count' }]);

connect(stream.value);


</script>

<template>
  <GMapMap :center="center" :zoom="zoom" style="width: 100%; height: 100%;">
    <GMapCluster>
      <GMapMarker v-for="(m, index) in records" :key="index" :position="{
        lng: (m as Record<string, any>).coordinates?.getX(),
        lat: (m as Record<string, any>).coordinates?.getY(),
      }" />
    </GMapCluster>
  </GMapMap>
</template>
