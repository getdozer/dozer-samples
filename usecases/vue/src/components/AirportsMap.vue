<script setup lang="ts">
import { EventType } from '@dozerjs/dozer/lib/esm/generated/protos/types_pb';
import { useDozerEndpointQuery } from '@dozerjs/dozer-vue';
const center = {
  lng: 50.993667602539063,
  lat: 50.7
};
const zoom = 4;
const { records } = useDozerEndpointQuery('airports_count', { query: { limit: 5000 }, watch: EventType.ALL });

</script>

<template>
  <GMapMap :center="center" :zoom="zoom" style="width: 100%; height: 100%;">
    <GMapCluster>
      <GMapMarker 
        v-for="(m, index) in records"
        :key="index"
        :position="{ 
          lng: (m as Record<string, any>).coordinates?.getX(), 
          lat: (m as Record<string, any>).coordinates?.getY(), 
        }"/>
    </GMapCluster>
  </GMapMap>
</template>
