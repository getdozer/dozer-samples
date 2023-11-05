<script setup lang="ts">
import { Order } from "@dozerjs/dozer";
import { useDozerEvent, useDozerQuery } from "@dozerjs/dozer-vue";
import { Type } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
import EmptyCard from "./EmptyCard.vue";

const { records, fields, connect } = useDozerQuery<Record<string, any>>('departures_count', { orderBy: { start: Order.ASC } });
const { stream } = useDozerEvent([{ endpoint: 'departures_count' }]);
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
            : (
              f.getName() === 'start'
                ? `${r[f.getName()]}:00 to ${r[f.getName()] + 4}:00 `
                : r[f.getName()]
            )
          }}
        </td>
      </tr>
    </tbody>
  </v-table>
  <EmptyCard v-if="fields === undefined" />
</template>