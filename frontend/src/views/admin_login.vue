<script setup>
// import store from '@/store'
import { RouterLink } from 'vue-router';
import router from '@/router'
</script>


<template>
  <div>
    <!-- Navbar -->
    <Navbar />

    <!-- Main Content -->
    <div class="container text-center mt-5">
      <div class="text-center mt-3 fst-italic fs-5">
        We handle the chaos of your house, so you never stop making it a home.
      </div>
      <h2 class="fw-bold">"HOUSE to HOME" Poem by LORRAINE M. HALLI</h2>

      <div class="row row-cols-1 row-cols-md-3 g-4 mt-4">
        <div class="col">
          <div class="bg-white p-4 rounded shadow-sm text-center">
            <strong>What is a house?</strong><br />
            It's brick and stone<br />
            and wood that's hard.<br />
            Some window glass<br />
            and perhaps a yard.<br />
            It's eaves and chimneys<br />
            and tile floors<br />
            and stucco and roof<br />
            and lots of doors.
          </div>
        </div>
        <div class="col">
          <div class="bg-white p-4 rounded shadow-sm text-center">
            <strong>What is a home?</strong><br />
            It's loving and family<br />
            and doing for others.<br />
            It's brothers and sisters<br />
            and fathers and mothers.<br />
            It's unselfish acts<br />
            and kindly sharing<br />
            and showing your loved ones<br />
            you're always caring.
          </div>
        </div>
        <div class="col d-flex flex-column justify-content-center align-items-center">
          <h4><strong>Admin Login</strong></h4>
          <form @submit.prevent="handleLogin" class="w-100">
            <div class="d-flex align-items-center mb-3">
              <label for="email" class="form-label me-2 mb-0" style="width: 100px;">Email</label>
              <input v-model="email" type="email" name="email" class="form-control" id="email" required />
            </div>
            <div class="d-flex align-items-center mb-3">
              <label for="password" class="form-label me-2 mb-0" style="width: 100px;">Password</label>
              <input v-model="password" type="password" name="password" class="form-control" id="password" required />
            </div>
            <div>
              <button type="submit" class="btn btn-primary">Log in</button>
            </div>
          </form>
          <div class="mt-3">
            Forgot credentials? <router-link to="#">Contact Developer</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray text-black text-center py-3 mt-5">
      <div class="container">
        <p class="mb-1">&copy; 2025 H2H. All rights reserved.</p>
        <p>
          <router-link to="#" class="text-black text-decoration-none">About Us</router-link> |
          <router-link to="#" class="text-black text-decoration-none">Services</router-link> |
          <router-link to="#" class="text-black text-decoration-none">Contact</router-link>
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import Navbar from "./nav.vue"; 

export default {
  name: "AdminLogin",
  components: {
    Navbar,
  },
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
        const loginData = {
            email: this.email,
            password: this.password
        };

        try {
            
            const response = await fetch('http://localhost:5000/admin_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            });

            const data = await response.json(); 

            if (response.ok) {
                
                console.log('Login successful:', data);
                
                localStorage.setItem('access_token', data[0].access_token);
                localStorage.setItem('user', JSON.stringify(data[1]));
                
                localStorage.setItem('role', data[0].role)
                this.$router.push('/admin_dashboard');
            } else {
                
                console.error('Login failed:', data.message);
                alert(`Login failed: ${data.message}`);
                
                this.$router.push('/')
            }
        } catch (error) {
            
            console.error('Error:', error);
            
        }
    }
  },
};
</script>