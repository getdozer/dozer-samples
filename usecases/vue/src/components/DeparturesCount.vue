<script setup lang="ts">
import { Order } from "@dozerjs/dozer";
import { useDozerEndpoint } from "@dozerjs/dozer-vue";
import { EventType, Type } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
import EmptyCard from "./EmptyCard.vue";

const { records, fields } = useDozerEndpoint('departures_count', {
  query: { orderBy: { start: Order.ASC } },
  watch: EventType.ALL,
});

</script> 

<template>
  <v-table v-if="fields">
    <thead>
      <tr>
        <th v-for="f in fields" :key="f.getName()">
          {{ f.getName() }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="r in records" :key="(r as Record<string, any>)[fields[0].getName()]">
        <td v-for="f in fields" :key="f.getName()">
          {{ 
            f.getTyp() === Type.POINT 
              ? `${(r as Record<string, any>)[f.getName()].getX()}, ${(r as Record<string, any>)[f.getName()].getY()}` 
              : (
                f.getName() === 'start'
                  ? `${(r as Record<string, any>)[f.getName()]}:00 to ${(r as Record<string, any>)[f.getName()] + 4}:00 `
                  : (r as Record<string, any>)[f.getName()] 
              )
          }}
        </td>
      </tr>
    </tbody>
  </v-table>
  <EmptyCard v-if="fields === undefined"/>
</template>