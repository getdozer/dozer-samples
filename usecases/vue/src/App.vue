<script setup lang="ts">
import { DozerProvider } from '@dozerjs/dozer-vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <header class="app-header">
    <img src="/logo.svg" className="App-logo" alt="logo" />
  </header>
  <main class="app-content">
    <DozerProvider :value="{
      serverAddress: 'http://localhost:62998',
    }">
      <RouterView />
    </DozerProvider>
  </main>
</template>

<style scoped>
.app-logo {
  height: 10vmin;
  pointer-events: none;
  padding: 10px;
}

.app-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
  text-align: center;
  margin-bottom: 16px;
}

.app-content {
  flex: 1;
}
</style>
