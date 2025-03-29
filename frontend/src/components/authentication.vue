<template>
    <div class="authentication">
        <header class="header">
            <Logo />
        </header>

        <main class="main-content">
            <section class="auth-section">
                <h2>{{ isLogin ? 'Welcome Back!' : 'Create Your Account' }}</h2>
                <div class="auth-container">
                    <div class="auth-card">
                        <!-- Login Form -->
                        <form v-if="isLogin" class="auth-form" @submit.prevent="handleLogin">
                            <div class="form-group">
                                <label for="userId">User ID</label>
                                <input 
                                    type="text" 
                                    id="userId" 
                                    class="form-input"
                                    v-model="userId"
                                    placeholder="Enter your User ID"
                                    required
                                />
                            </div>
                            
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input 
                                    type="password" 
                                    id="password" 
                                    class="form-input"
                                    v-model="password"
                                    placeholder="Enter your password"
                                    required
                                />
                            </div>

                            <button type="submit" class="submit-btn">Login</button>
                        </form>

                        <!-- Registration Form -->
                        <form v-else class="auth-form" @submit.prevent="handleRegister">
                            <div class="form-group">
                                <label for="newUserId">User ID</label>
                                <input 
                                    type="text" 
                                    id="newUserId" 
                                    class="form-input"
                                    v-model="registerData.userId"
                                    placeholder="Create a unique User ID"
                                    required
                                />
                            </div>
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input 
                                    type="text" 
                                    id="name" 
                                    class="form-input"
                                    v-model="registerData.name"
                                    placeholder="Enter your name"
                                    required
                                />
                            </div>
                            
                            <div class="form-group">
                                <label for="newPassword">Password</label>
                                <input 
                                    type="password" 
                                    id="newPassword" 
                                    class="form-input"
                                    v-model="registerData.password"
                                    placeholder="Create a password"
                                    required
                                />
                            </div>

                            <div class="form-group">
                                <label for="confirmPassword">Confirm Password</label>
                                <input 
                                    type="password" 
                                    id="confirmPassword" 
                                    class="form-input"
                                    v-model="registerData.confirmPassword"
                                    placeholder="Confirm your password"
                                    required
                                />
                            </div>

                            <div class="form-group">
                                <label for="weight">Weight (kg)</label>
                                <input 
                                    type="number" 
                                    id="weight" 
                                    class="form-input"
                                    v-model="registerData.weight"
                                    placeholder="Enter your weight in kg"
                                    min="30"
                                    max="200"
                                    required
                                />
                            </div>

                            <div class="form-group">
                                <label>Fitness Goal</label>
                                <div class="toggle-container">
                                    <button 
                                        type="button"
                                        class="toggle-btn"
                                        :class="{ active: registerData.goal === 'lose' }"
                                        @click="registerData.goal = 'lose'"
                                    >
                                        <span class="goal-icon">🏃‍♂️</span>
                                        <div class="goal-text">
                                            <span class="goal-title">Lose Weight</span>
                                            <span class="goal-desc">Burn fat & get lean</span>
                                        </div>
                                    </button>
                                    <button 
                                        type="button"
                                        class="toggle-btn"
                                        :class="{ active: registerData.goal === 'gain' }"
                                        @click="registerData.goal = 'gain'"
                                    >
                                        <span class="goal-icon">💪</span>
                                        <div class="goal-text">
                                            <span class="goal-title">Gain Muscles</span>
                                            <span class="goal-desc">Build strength & mass</span>
                                        </div>
                                    </button>
                                </div>
                            </div>

                            <button type="submit" class="submit-btn">Create Account</button>
                        </form>

                        <!-- Error Message -->
                        <p v-if="error" class="error-message">{{ error }}</p>

                        <!-- Toggle Links -->
                        <div class="auth-links">
                            <template v-if="isLogin">
                                <a href="#" class="forgot-password">Forgot Password?</a>
                                <a href="#" class="register" @click.prevent="toggleView">Create New Account</a>
                            </template>
                            <template v-else>
                                <p>Already have an account? <a href="#" @click.prevent="toggleView">Login here</a></p>
                            </template>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>
</template>

<script>
import Logo from './logo.vue'
import axios from 'axios';


export default {
    name: 'Authentication',
    components: {
        Logo,
    },
    data() {
        return {
            isLogin: true,  
            userId: '',
            password: '',
            registerData: {
                userId: '',
                name: '',
                password: '',
                confirmPassword: '',
                weight: '',
                goal: 'lose'
            },
            error: ''
        }
    },
    methods: {
        toggleView() {
            this.isLogin = !this.isLogin;
            this.error = '';
        },
        async handleLogin() {
            try {
                const response = await axios.post('http://localhost:5001/login', {
                    userId: this.userId,
                    password: this.password
                });

                if (response.data.code === 200) {
                    localStorage.setItem('user', JSON.stringify(response.data.data));
                    this.$router.push('/homepage');
                } else {
                    this.error = response.data.message;
                }
            } catch (error) {
                this.error = error.response?.data?.message || 'An error occurred during login';
            }
        },
        async handleRegister() {
            if (this.registerData.password !== this.registerData.confirmPassword) {
                this.error = 'Passwords do not match';
                return;
            }

            try {
                const response = await axios.post(`http://localhost:5001/user/${this.registerData.userId}`, {
                    name: this.registerData.name,
                    weight: parseFloat(this.registerData.weight),
                    password: this.registerData.password,
                    goal: this.registerData.goal === 'lose' ? 'Lose Weight' : 'Gain Muscles'
                });
                
                if (response.data.code === 201) {
                    this.isLogin = true;
                    this.error = 'Registration successful! Please login.';
                } else {
                    this.error = response.data.message;
                }
            } catch (error) {
                console.error('Registration error:', error.response?.data || error);
                this.error = error.response?.data?.message || 'An error occurred during registration';
            }
        }
    }
}
</script>

<style scoped>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .authentication {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        min-height: 100vh;
        background: #333;
    }

    .header {
        position: relative;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 80px;
        background: #333;
        border-bottom: 1px solid #444;
    }

    .main-content {
        position: relative;
        width: 100%;
        padding: 40px 80px;
        background: #333;
    }

    .auth-section {
        position: relative;
        width: 100%;
        max-width: 500px;
        margin: 40px auto;
    }

    .auth-card {
        background: #444;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .auth-form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    label {
        color: white;
        font-size: 14px;
        font-weight: 500;
    }

    .form-input {
        padding: 12px;
        border: 1px solid #555;
        border-radius: 8px;
        background: #333;
        color: white;
        font-size: 16px;
    }

    .form-input:focus {
        outline: none;
        border-color: #42b983;
    }

    .form-input::placeholder {
        color: #888;
    }

    .submit-btn {
        background: #42b983;
        color: white;
        padding: 12px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .submit-btn:hover {
        background: #3aa876;
    }

    .auth-links {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #555;
    }

    .auth-links a {
        color: #42b983;
        text-decoration: none;
        font-size: 14px;
    }

    .auth-links a:hover {
        text-decoration: underline;
    }

    h2 {
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    @media (max-width: 1024px) {
        .header,
        .main-content {
            padding: 20px 40px;
        }
    }

    @media (max-width: 768px) {
        .header,
        .main-content {
            padding: 20px;
        }

        .auth-card {
            padding: 30px;
        }
    }

    @media (max-width: 480px) {
        .auth-links {
            flex-direction: column;
            gap: 15px;
            text-align: center;
        }
    }


    :deep(.logo h1) {
        color: #42b983;  
        font-size: 24px;
    }

    :deep(.logo a) {
        color: #42b983;
        text-decoration: none;
    }

    .error-message {
        color: #ff6b6b;
        text-align: center;
        margin-top: 15px;
        font-size: 14px;
    }

    .toggle-container {
        display: flex;
        gap: 15px;
        margin-top: 10px;
        width: 100%;
    }

    .toggle-btn {
        flex: 1;
        display: flex;
        align-items: center;
        padding: 15px;
        border: 2px solid #555;
        background: #333;
        color: white;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }

    .toggle-btn:hover {
        background: #444;
        transform: translateY(-2px);
    }

    .toggle-btn.active {
        background: #42b983;
        border-color: #42b983;
        box-shadow: 0 4px 12px rgba(66, 185, 131, 0.2);
    }

    .toggle-btn.active:hover {
        background: #3aa876;
    }

    .goal-icon {
        font-size: 24px;
        margin-right: 12px;
    }

    .goal-text {
        display: flex;
        flex-direction: column;
    }

    .goal-title {
        font-weight: 600;
        font-size: 14px;
    }

    .goal-desc {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 2px;
    }

    @media (max-width: 480px) {
        .toggle-container {
            flex-direction: column;
        }

        .toggle-btn {
            width: 100%;
        }
    }
</style> 