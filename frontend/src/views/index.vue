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
          <img src="@/assets/logo.jpg" alt="Logo" class="img-fluid mb-2" width="180" height="120" />
          <p><strong>Our service professionals are just a few clicks away!</strong></p>
          <router-link to="/customer_login" class="btn btn-primary mt-0 mb-0">Book Now</router-link>
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
import Navbar from "./nav.vue"; // Ensure this path matches your project structure

export default {
  name: "Index",
  components: {
    Navbar,
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");

    // Check if the token exists
    if (token) {
      // Redirect based on the role
      if (role === "Customer") {
        this.$router.push('/customer_dashboard');
      } else if (role === "Professional") {
        this.$router.push('/professional_dashboard');
      } else if (role === "Admin") {
        this.$router.push('/admin_dashboard');
      } else {
        // Default redirect if role is not recognized
        this.$router.push('/');
      }
    }
  },
};
</script>

