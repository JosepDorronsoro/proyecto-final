<template>
  <div class="game-card">
    <img :src="game.image || 'placeholder.jpg'" :alt="game.name" />
    <h3>{{ game.name }}</h3>
    <p>{{ game.description }}</p>
    <p><strong>Año:</strong> {{ game.year }}</p>

    <button
      v-if="game.islocal"
      @click="$emit('abrir-local', game)"
      class="play-link"
    >
      Jugar (Local)
    </button>
    
    <a
      v-else-if="game.url"
      :href="game.url"
      target="_blank"
      rel="noopener"
      class="play-link"
    >
      Más Información
    </a>
    
    <span v-else class="play-link-disabled">No disponible</span>

    <div v-if="store.state.isAdmin" class="admin-buttons">
      <button @click="$emit('edit', game.id)" class="edit-btn">Editar</button>
      <button @click="$emit('delete', game.id)" class="delete-btn">Eliminar</button>
    </div>
  </div>
</template>

<script setup>
import store from '../store'

defineProps({
  game: Object
})

defineEmits(['abrir-local', 'edit', 'delete'])
</script>

<style scoped>
.game-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.game-card:hover {
  transform: translateY(-5px);
  border-color: var(--accent-primary);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.game-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  background-color: #eee;
  border: 1px solid var(--border-color);
}

.game-card p {
  color: var(--text-secondary);
  font-family: 'Poppins', sans-serif;
  text-shadow: none;
}
.game-card p strong {
  color: var(--text-primary);
}

.play-link {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  border: none;
}
.play-link-disabled {
  display: inline-block;
  margin-top: 0.5rem;
  background: var(--border-color);
  color: var(--text-secondary);
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
}
.admin-buttons {
  border-top: 1px solid var(--border-color);
  margin-top: 1rem;
  padding-top: 1rem;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}
.admin-buttons button {
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  transition: all 0.2s ease;
}
.edit-btn {
  background-color: #ffc107;
  color: #333;
}
.edit-btn:hover {
  box-shadow: 0 0 10px #ffc107;
}
.delete-btn {
  background-color: var(--color-error);
  color: white;
}
.delete-btn:hover {
  box-shadow: 0 0 10px var(--color-error);
}
</style>