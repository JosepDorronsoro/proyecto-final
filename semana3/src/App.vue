<template>
  <div id="app" class="app-root">
    <header class="top">
      <h1>Juegos Jugosos</h1>
      <p>¡Juega y Disfruta!.</p>
    </header>

    <NavBar />

    <main>
      <router-view />
    </main>

    <footer class="site-footer">
      Portal de Juegos © 2025 — Desarrollado por <strong>Pablo&Ivan</strong>
    </footer>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script>

<style>

.app-root {
  max-width: 1100px;
  margin: 2rem auto;
  padding: 0 1rem;
}
.top h1 {
  margin: 0;
}
.site-footer {
  text-align: center;
  margin-top: 2rem;
  color: #666;
}
body {
  background: #f6f8fb;
  font-family: Inter, system-ui, Arial;
}

</style>