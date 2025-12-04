import { reactive, readonly } from 'vue'

const state = reactive({
  isLoggedIn: false,
  username: null,
  isAdmin: false
})

const actions = {
  
  clearSession() {
    state.isLoggedIn = false
    state.username = null
    state.isAdmin = false
  },

  async checkSession() {
    try {
      
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const res = await fetch(`${API_URL}/api/profile`, { credentials: 'include'  })

      if (res.ok) {
        const data = await res.json()
        state.isLoggedIn = true
        state.username = data.username
        state.isAdmin = data.username === 'admin'
      } else {
        actions.clearSession() 
      }
      return state.isLoggedIn

    } catch (error) {
      console.error('Error checking session:', error)
      actions.clearSession() 
      return false
    }
  }, 

  setUser(userData) {
    state.isLoggedIn = true
    state.username = userData.username
    state.isAdmin = userData.isAdmin
  }

}

export default {
  state: readonly(state),
  ...actions
}
