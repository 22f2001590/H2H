<template>
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/professional_dashboard">Professional Dashboard</a>
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <a class="nav-link" :href="`/professional_history/${user.id}`">My Work History</a>
          </li>
        </ul>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="collapsibleNavbar">
          <ul class="navbar-nav ms-auto"> 
            <li class="nav-item">
              <a class="nav-link" :href="`/user_profile/${user.id}`">{{ user.name }}: {{ user.service}}</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="javascript:void(0);" @click="handleLogout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    data() {
    return {
      user: {
        id: "", // Replace with actual user ID
        name: "", // Replace with actual user name
        service: ""
      },
    };
  },
  mounted() {
    // Fetch user data when the component is mounted
    const user = JSON.parse(localStorage.getItem('user'))
    this.user.id = user.id;
    this.user.name = user.name;
    this.user.service = user.service;

  },
  methods:{
    handleLogout() {
      // Clear all local storage
      localStorage.clear();

      // Optional: Log a message for debugging
      console.log('Local storage cleared. Logging out...');

      // Redirect to the logout endpoint
      this.$router.push('/'); // Ensure your router is configured for this path
    }
  }
  };
  </script>
  
  <style scoped>
  /* Add any custom styles here */
  </style>
  