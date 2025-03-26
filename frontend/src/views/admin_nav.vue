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

</template>

<script>
export default {
  name: "AdminNavbar",
  
  methods: {
    handleLogout() {
      
      localStorage.clear();

      
      console.log('Local storage cleared. Logging out...');

      
      this.$router.push('/'); 
    }
  },
};
</script>
