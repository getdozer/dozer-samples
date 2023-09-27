<script setup lang="ts">
import { useDozerEndpoint } from "@dozerjs/dozer-vue";
import { EventType } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
defineProps<{
  msg: string
}>()

const { fields, records, count } = useDozerEndpoint('airports_count', { watch: EventType.ALL })
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ count }}</h1>
    <h3>
      You’ve successfully created a project with
      <table>
        <thead>
          <tr>
            <th v-for="f in fields" :key="f.getName()">{{ f.getName() }}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td v-for="r in records" :key="r.toString()">{{ r.toString() }}</td>
          </tr>
        </tbody>
      </table>
      
      <a href="https://vitejs.dev/" target="_blank" rel="noopener">Vite</a> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>. What's next?
    </h3>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
