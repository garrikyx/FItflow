<!-- frontend/src/components/NavBar.vue -->
<template>
    <nav class="nav-menu">
      <router-link to="/homepage" class="nav-link">
        <span class="nav-emoji">🏠</span>
        Home
      </router-link>
      <!-- <router-link to="/weather" class="nav-link">Weather</router-link> -->
      <!-- <router-link to="/meals" class="nav-link">Meals</router-link> -->
      <router-link to="/leaderboard" class="nav-link">
        <span class="nav-emoji">🏆</span>
        Leaderboard
      </router-link>
      <div v-if="isLoggedIn">
        <button @click="logout" class="nav-link logout-btn">
          Logout
        </button>
      </div>
      <div v-else>
        <router-link to="/">Login</router-link>
      </div>
    </nav>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('user')
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0.5rem 1rem;
}

.brand {
  text-decoration: none;
  color: #42b983;
  font-weight: 600;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.brand-emoji {
  font-size: 1.2rem;
}

.nav-menu {
  display: flex;
  gap: 12px;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: white;
  font-weight: 500;
  font-size: 0.9rem;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link:hover {
  color: #42b983;
  background: rgba(66, 185, 131, 0.1);
}

.nav-emoji {
  font-size: 16px;
}

.logout-btn {
  background: transparent;
  border: 1px solid #42b983;
  cursor: pointer;
  font-size: 0.9rem;
  color: #42b983;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: #42b983;
  color: white;
}

.router-link-active {
  color: #42b983;
  background: rgba(66, 185, 131, 0.1);
  font-weight: 500;
}
</style>