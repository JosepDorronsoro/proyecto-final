<template>
  <div class="form-container">
    <h1>{{ isEditing ? 'Editar Juego' : 'Añadir Nuevo Juego' }}</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">Nombre:</label>
        <input type="text" id="name" v-model="form.name" required>
      </div>
      <div class="form-group">
        <label for="description">Descripción:</label>
        <textarea id="description" v-model="form.description" required></textarea>
      </div>
      <div class="form-group">
        <label for="year">Año:</label>
        <input type="number" id="year" v-model.number="form.year">
      </div>
      <div class="form-group">
        <label for="image">URL de la Imagen:</label>
        <input type="text" id="image" v-model="form.image">
      </div>
      <div class="form-group">
        <label for="url">URL (Wikipedia, etc.):</label>
        <input type="text" id="url" v-model="form.url">
      </div>
      <div class="form-group check-group">
        <input type="checkbox" id="islocal" v-model="form.islocal">
        <label for="islocal">¿Es un juego local?</label>
      </div>
      <div class="form-buttons">
        <router-link to="/games" class="cancel-button">Cancelar</router-link>
        <button type="submit" class="submit-button">
          {{ isEditing ? 'Guardar Cambios' : 'Añadir Juego' }}
        </button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const props = defineProps({
  id: { type: String, default: null } 
})

const isEditing = ref(false)
const error = ref(null)
const form = reactive({
  name: '',
  description: '',
  year: null,
  image: '',
  url: '',
  islocal: false
})

onMounted(async () => {
  if (props.id) {
    isEditing.value = true
    try {
      const res = await fetch(`${API_URL}/api/juego/${props.id}`, { credentials: 'include' })
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || 'No se pudo cargar el juego');
      }
      const data = await res.json()
    
      form.name = data.name
      form.description = data.description
      form.year = data.year
      form.image = data.image
      form.url = data.url
      form.islocal = data.islocal
    } catch (err) {
      error.value = err.message
    }
  }
})

async function handleSubmit() {
  error.value = null
  try {
    const url = isEditing.value 
      ? `${API_URL}/api/editar_juego/${props.id}` 
      : `${API_URL}/api/anadir_juego`
      
    const method = isEditing.value ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(form)
    })
    
    const data = await res.json()
    if (!res.ok) throw new Error(data.error)

    router.push({ name: 'GameList' })

  } catch (err) {
    error.value = err.message
  }
}
</script>

<style scoped>

.auth-form, .form-container {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea { 
  width: 100%; 
  padding: 10px; 
  border: 1px solid #ddd; 
  border-radius: 4px; 
  box-sizing: border-box;
}
.form-group textarea { resize: vertical; min-height: 80px; }
.check-group { display: flex; align-items: center; }
.check-group input { width: auto; margin-right: 10px; }
.check-group label { margin-bottom: 0; }
.form-buttons { display: flex; gap: 10px; margin-top: 1rem; }
.form-buttons button, .form-buttons a { flex: 1; padding: 10px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; text-decoration: none; text-align: center; }
.submit-button { background-color: #28a745; color: white; }
.cancel-button { background-color: #6c757d; color: white; }
.error { color: #dc3545; }
</style>
