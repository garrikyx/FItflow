<template>
    <div class="login-container">
        <div class="logo-wrapper">
            <Logo class="auth-logo" />
        </div>
        <h1 style="text-align: center;">Login</h1>
        <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
            <label for="userId">User ID:</label>
            <input 
            type="text" 
            id="userId" 
            v-model="userId" 
            required
            >
        </div>
        
        <div class="form-group">
            <label for="password">Password:</label>
            <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
            >
        </div>

        <div v-if="error" class="error-message">
            {{ error }}
        </div>

        <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
import Logo from './Logo.vue'

export default {
    name: 'Login',
    components: {
        Logo
    },
    data() {
        return {
        userId: '',
        password: '',
        error: ''
        }
    },
    methods: {
        async handleLogin() {
        try {
            const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: this.userId,
                password: this.password
            })
            });

            const data = await response.json();

            if (data.code === 200) {
            // Store user data
            localStorage.setItem('user', JSON.stringify(data.data));
            // Redirect to homepage or dashboard
            this.$router.push('/homepage');
            } else {
            this.error = data.message;
            }
        } catch (err) {
            this.error = 'An error occurred during login';
        }
        }
    }
}
</script>

<style scoped>
    .login-container {
    max-width: 400px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    }

    .logo-wrapper {
    text-align: center;
    margin-bottom: 20px;
    }

    .login-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
    }

    .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    }

    input {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    }

    button {
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    }

    button:hover {
    background-color: #45a049;
    }

    .error-message {
    color: red;
    text-align: center;
    }

    .logo-wrapper :deep(.logo h1) {
        color: #42b983 !important;
    }

    .logo-wrapper :deep(svg) {
        fill: #42b983;
    }

    .auth-logo {
        color: #42b983;
    }
</style> 