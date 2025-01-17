<template>
  <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <div class="container-fluid d-flex justify-content-between">
      <!-- Brand -->
      <a class="navbar-brand" href="/admin_dashboard">Admin Dashboard</a>

      <!-- Centered Navigation Links -->
      <div class="navbar-nav mx-auto">
        <a class="nav-link" href="/users">Users</a>
        <a class="nav-link" href="/services">Services</a>
        <a class="nav-link" href="/app_summary">App Summary</a>
        
      </div>

      <!-- Right Navigation -->
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="javascript:void(0);" @click="handleLogout">Logout</a>
        </li>
      </ul>
    </div>
  </nav>

  <!-- Alert Section -->
  <div class="container mt-3">
    <div v-if="messages.length" class="alert alert-info alert-dismissible fade show" role="alert">
      {{ messages[0] }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"
        @click="clearMessages"></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminNavbar",
  props: {
    messages: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    
    clearMessages() {
      // Clear messages after the alert is dismissed
      this.$emit("clear-messages");
    },
    handleLogout() {
      // Clear all local storage
      localStorage.clear();

      // Optional: Log a message for debugging
      console.log('Local storage cleared. Logging out...');

      // Redirect to the logout endpoint
      this.$router.push('/'); // Ensure your router is configured for this path
    }
  },
};
</script>

<style scoped>
/* Add any scoped styles if needed */
</style>