<template>
  <nav class="main-nav">
    <div v-if="store.state.isLoggedIn" class="nav-content">
      <div class="nav-links">
        <router-link to="/games">Catálogo de Juegos</router-link>
        
        <router-link v-if="store.state.isAdmin" to="/games/add" class="admin-link">
          Añadir Juego
        </router-link>
      </div>

      <div class="user-info">
        <span>Bienvenido, <strong>{{ store.state.username }}</strong></span>
        <span class="separator">|</span>
        <a href="#" @click.prevent="handleLogout" class="logout-button">Cerrar Sesión</a>
      </div>
    </div>
    
    <div v-else class="nav-content">
      <span>Debes iniciar sesión para ver los juegos.</span>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import store from '../store'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const router = useRouter()

async function handleLogout() {
  try {
    await fetch(`${API_URL}/api/logout`, { credentials: 'include' })
  } catch (error) {
    console.error('Error during logout:', error)
  } finally {
    store.clearSession()
    router.push({ name: 'Login' })
  }
}
</script>

<style scoped>
.main-nav {
  background: var(--bg-secondary);
  color: var(--text-primary);
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-links a {
  color: var(--text-primary);
  text-decoration: none;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.nav-links a:hover {
  color: var(--accent-primary);
  text-shadow: 0 0 8px var(--accent-primary);
}

.nav-links a.router-link-exact-active {
  color: var(--accent-primary);
}

.admin-link {
  background-color: var(--color-success);
  color: var(--bg-primary) !important;
  font-size: 0.9rem;
}
.admin-link:hover {
  color: var(--bg-primary) !important;
  box-shadow: 0 0 10px var(--color-success);
}


.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: 'Poppins', sans-serif;
}

.user-info span {
  color: var(--text-secondary);
}

.user-info strong {
  color: var(--accent-hover);
  font-weight: 600;
}

.separator {
  color: var(--border-color);
}

.logout-button {
  color: var(--color-error);
  text-decoration: none;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-button:hover {
  text-shadow: 0 0 8px var(--color-error);
}
</style>
