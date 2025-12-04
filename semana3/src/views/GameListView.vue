<template>
  <section class="games-panel">
    <div class="controls-bar">
      <input
        type="text"
        v-model="searchTerm"
        placeholder="Buscar juego..."
        class="search-box"
      />

      <select v-model="sortOrder" class="sort-select">
        <option value="asc">Ordenar por año (asc)</option>
        <option value="desc">Ordenar por año (desc)</option>
      </select>
    </div>

    <div v-if="isLoading" class="loading">Cargando juegos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="filteredAndSortedGames.length === 0" class="loading">
      No se encontraron juegos.
    </div>
    
    <div v-else class="games-grid">
      <GameCard
        v-for="game in filteredAndSortedGames"
        :key="game.id"
        :game="game"
        @abrir-local="mostrarJuegoLocal"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>

    <div v-if="juegoLocalVisible" class="local-game">
      <h2>{{ juegoLocalVisible.name }}</h2>
      <TicTacToe />
      <button @click="cerrarJuegoLocal" class="close-btn">Cerrar</button>
    </div>

    <FooterKeywords :games="filteredAndSortedGames" @keyword-click="setSearchTerm" />
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import GameCard from '../components/GameCard.vue'
import FooterKeywords from '../components/FooterKeywords.vue'
import TicTacToe from '../components/TicTacToe.vue'

const router = useRouter()

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const allGames = ref([])
const isLoading = ref(true)
const error = ref(null)

const searchTerm = ref('')
const sortOrder = ref('asc')
const juegoLocalVisible = ref(null)

onMounted(async () => {
  isLoading.value = true
  error.value = null
  try {
    const res = await fetch(`${API_URL}/api/listar_juegos`, { credentials: 'include' })
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.error || 'Error al cargar los juegos');
    }
    allGames.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
})

const filteredAndSortedGames = computed(() => {
  const filtered = allGames.value.filter(game =>
    game.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    (game.description && game.description.toLowerCase().includes(searchTerm.value.toLowerCase()))
  )

  return filtered.sort((a, b) => {
    const yearA = a.year || 0;
    const yearB = b.year || 0;
    return sortOrder.value === 'asc' ? yearA - yearB : yearB - yearA;
  })
})

function handleEdit(gameId) {
  router.push({ name: 'GameEdit', params: { id: gameId } })
}

async function handleDelete(gameId) {
  if (!confirm('¿Estás seguro de que quieres eliminar este juego?')) return

  try {
    const res = await fetch(`${API_URL}/api/eliminar_juego/${gameId}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error)
    
    allGames.value = allGames.value.filter(g => g.id !== gameId)

  } catch (err) {
    alert(`Error: ${err.message}`)
  }
}

function mostrarJuegoLocal(game) {
  juegoLocalVisible.value = game
}

function cerrarJuegoLocal() {
  juegoLocalVisible.value = null
}

function setSearchTerm(keyword) {
  searchTerm.value = keyword
}
</script>

<style scoped>

.games-panel { display: flex; flex-direction: column; gap: 1.5rem; }
.controls-bar { display: flex; flex-direction: column; gap: 1rem; }
@media (min-width: 768px) {
  .controls-bar {
    flex-direction: row;
  }
}
.games-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem; }
.local-game { text-align: center; border-top: 2px solid #ddd; padding-top: 1rem; }
.search-box, .sort-select { 
  padding: 0.5rem; 
  font-size: 1rem; 
  border-radius: 8px; 
  border: 1px solid #ccc; 
  width: 100%; 
  box-sizing: border-box;
}
@media (min-width: 768px) {
  .search-box, .sort-select {
    width: 50%;
  }
}
.close-btn { margin-top: 1rem; background: #d9534f; color: white; padding: 0.5rem 1rem; border: none; border-radius: 6px; cursor: pointer; }
.close-btn:hover { background: #b52b27; }
.loading, .error { text-align: center; font-size: 1.2rem; padding: 2rem; }
.error { color: #dc3545; }
</style>

