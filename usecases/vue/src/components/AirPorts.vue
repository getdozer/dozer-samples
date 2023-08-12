<script setup lang="ts">
import { Type } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
import { useDozerEndpoint } from '@dozerjs/dozer-vue';
import EmptyCard from "./EmptyCard.vue";
const { records, fields } = useDozerEndpoint('airports');
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
              : (r as Record<string, any>)[f.getName()] 
          }}
        </td>
      </tr>
    </tbody>
  </v-table>
  <EmptyCard v-if="fields === undefined"/>
</template>