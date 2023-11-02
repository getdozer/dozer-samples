<script setup lang="ts">
import { Type } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
import { useDozerEvent, useDozerQuery } from '@dozerjs/dozer-vue';
import EmptyCard from "./EmptyCard.vue";
const { records, fields, connect } = useDozerQuery<Record<string, any>>('airports');
const { stream } = useDozerEvent([{ endpoint: 'airports' }]);
connect(stream.value);
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
      <tr v-for="r in records" :key="r.__dozer_record_id">
        <td v-for="f in fields" :key="f.getName()">
          {{
            f.getTyp() === Type.POINT
            ? `${r[f.getName()].getX()}, ${r[f.getName()].getY()}`
            : r[f.getName()]
          }}
        </td>
      </tr>
    </tbody>
  </v-table>
  <EmptyCard v-if="fields === undefined" />
</template>