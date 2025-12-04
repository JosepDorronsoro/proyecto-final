<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="auth-form">
      <h2>Iniciar Sesión</h2>
      <div class="form-group">
        <label for="login-username">Usuario:</label>
        <input type="text" id="login-username" v-model="loginForm.username" required>
      </div>
      <div class="form-group">
        <label for="login-password">Contraseña:</label>
        <input type="password" id="login-password" v-model="loginForm.password" required>
      </div>
      <button type="submit">Entrar</button>
      <p v-if="loginError" class="error">{{ loginError }}</p>
    </form>

    <form @submit.prevent="handleRegister" class="auth-form">
      <h2>Registrarse</h2>
      <div class="form-group">
        <label for="reg-username">Usuario:</label>
        <input type="text" id="reg-username" v-model="registerForm.username" required>
      </div>
      <div class="form-group">
        <label for="reg-password">Contraseña:</label>
        <input type="password" id="reg-password" v-model="registerForm.password" required>
      </div>
      <button type="submit">Registrar</button>
      <p v-if="registerError" class="error">{{ registerError }}</p>
      <p v-if="registerSuccess" class="success">{{ registerSuccess }}</p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import store from '../store'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const router = useRouter()

const loginForm = reactive({ username: '', password: '' })
const loginError = ref(null)

async function handleLogin() {

  loginError.value = null

  try {
    const res = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(loginForm)
    })
    
    const data = await res.json()
    if (!res.ok) throw new Error(data.error)

    store.setUser(data.user) 
    
    router.push({ name: 'GameList' });

  } catch (error) {
    
    console.error('ERROR DETALLADO DEL LOGIN:', error); 
    loginError.value = error.message; 
    alert('Ha ocurrido un error: ' + error.message);
  }
}

const registerForm = reactive({ username: '', password: '' })
const registerError = ref(null)
const registerSuccess = ref(null)

async function handleRegister() {
  registerError.value = null
  registerSuccess.value = null
  try {
    const res = await fetch(`${API_URL}/api/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerForm)
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error)
    
    registerSuccess.value = data.message + '. Ahora puedes iniciar sesión.'
    registerForm.username = ''
    registerForm.password = ''

  } catch (error) {
    registerError.value = error.message
  }
}
</script>

<style scoped>
.login-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .login-container {
    grid-template-columns: 1fr 1fr;
  }
}

.auth-form, .form-container {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; }
.form-group input { 
  width: 100%; 
  padding: 0.8rem; 
  border: 1px solid #ccc; 
  border-radius: 4px; 
  box-sizing: border-box;
}
.auth-form button { width: 100%; padding: 0.8rem; background: #007bff; color: white; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }
.auth-form button:hover { background: #0056b3; }
.error { color: #dc3545; }
.success { color: #28a745; }
</style>

