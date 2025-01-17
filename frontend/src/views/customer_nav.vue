<template>
  <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="/customer_dashboard">Customer Dashboard</a>
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <a class="nav-link" :href="`/customer_history/${user.id}`">My Booking History</a>
        </li>
      </ul>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="collapsibleNavbar">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" :href="`/user_profile/${user.id}`">{{ user.name }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="javascript:void(0);" @click="handleLogout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- <div class="container mt-3">
    <div v-if="messages.length > 0" class="alert alert-info alert-dismissible fade show" role="alert">
      {{ messages[0] }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeMessage"></button>
    </div>
  </div> -->
</template>

<script>
export default {
  data() {
    return {
      user: {
        id: "", // Replace with actual user ID
        name: "", // Replace with actual user name
      },
    };
  },
  mounted() {
    // Fetch user data when the component is mounted
    const user = JSON.parse(localStorage.getItem('user'))
    this.user.id = user.id;
    this.user.name = user.name;

  },
  methods: {
    closeMessage() {
      // Clear the first message after the close button is clicked
      this.messages.shift();
    },
    fetchUserData() {
      // Fetch user data from the API
      // Replace the placeholder data with actual user data
      this.user.name = localStorage.getItem('user.name');
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
/* Add any necessary styles here */
</style>