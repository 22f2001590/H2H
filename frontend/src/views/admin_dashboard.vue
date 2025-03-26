<template>
  <div>
    <!-- Admin Navigation -->
    <AdminNav />
    
    <div class="container mt-4">
      <div class="row">
        <!-- Live Requests Section -->
        <div class="col-md-8">
          <h4 class="mb-3">Live Requests</h4>
          <div class="list-group">
            <div v-for="lr in liveRequests" :key="lr.id" class="list-group-item">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div>
                  <h5 class="mb-0">{{ lr.service.name }}</h5>
                </div>
                <div class="text-end">
                  <small class="text-muted">
                    Scheduled at:
                    {{ formatDate(lr.needed_at) }} IST
                    IST
                  </small>
                </div>
              </div>
              <p class="mb-1">
                Status:
                <template v-if="lr.status === 'requested'">
                  <span class="text-danger">Requested</span> by
                  <a :href="`/user_profile/${lr.customer.id}`" class="text-primary">{{ lr.customer.name }}</a>
                </template>
                <template v-else-if="lr.status === 'accepted'">
                  <span class="text-danger">Requested</span> by
                  <a :href="`/user_profile/${lr.customer.id}`" class="text-primary">{{ lr.customer.name }}</a>,
                  <span class="text-warning">Accepted</span> by
                  <a :href="`/user_profile/${lr.professional.id}`" class="text-primary">{{ lr.professional.name }}</a>
                </template>
                <template v-else-if="lr.status === 'paid'">
                  <span class="text-danger">Requested</span> by
                  <a :href="`/user_profile/${lr.customer.id}`" class="text-primary">{{ lr.customer.name }}</a>,
                  <span class="text-warning">Accepted</span> by
                  <a :href="`/user_profile/${lr.professional.id}`" class="text-primary">{{ lr.professional.name }}</a>
                  <span class="text-success">, Amount Paid</span>
                </template>
                <template v-else>
                  <span class="text-danger">Not Closed</span>
                </template>
              </p>
            </div>
          </div>
        </div>

        <!-- Pending Actions Section -->
        <div class="col-md-4">
          <h4 class="my-3 text-center">Pending Actions</h4>
          <div class="list-group">
            <div v-for="u in inactiveUsers" :key="u.id" class="card mb-3 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="card-title mb-0">{{ u.name }}</h5>
                  <div class="btn-group">
                    <a :href="`/user_profile/${u.id}`" class="btn btn-warning btn-sm me-2">Profile</a>
                    <button @click="removeUser(u.id)" class="btn btn-danger btn-sm">
                      Remove
                    </button>
                  </div>

                </div>
                <template v-if="u.service_id === -1">
                  <form @submit.prevent="approveService(u.id)" class="mt-3">
                    <div class="form-group">
                      <label for="service" class="form-label d-block">
                        <a href="/services" class="btn btn-link p-0 text-decoration-none">+ Add Service</a>
                      </label>
                      <select v-model="selectedService" name="service" id="service" class="form-select" required>
                        <option value="-1">Create New Service</option>
                        <option v-for="s in services" :key="s.id" :value="s.id">{{ s.name }}</option>
                      </select>
                    </div>
                    <button type="submit" class="btn btn-success btn-sm w-100 mt-2">Approve Service</button>
                  </form>
                </template>
              </div>
            </div>
          </div>
        </div>

       
      </div>
    </div>
  </div>
</template>

<script>
import AdminNav from "./admin_nav.vue";

export default {
  name: "Admin",
  components: {
    AdminNav,
  },
  data() {
    return {
      selectedService: '-1',
      liveRequests: [],
      inactiveUsers: [],
      services: [], 
    };
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (!token || role !== "Admin") {
      this.$router.push('/');
    }
    this.fetchLiveRequests();
    this.fetchServices();
  },
  methods: {
    
    async approveService(u_id) {
      try {
        const body = {
          id: u_id,
          service: this.selectedService,
        };
        
        const response = await fetch('http://localhost:5000/approve', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
          body: JSON.stringify(body),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        this.fetchLiveRequests(); 
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to approve service. Please try again.');
      }
    },
    fetchServices() {
      fetch('http://localhost:5000/services', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        }).then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
          return response.json(); 
        })
        .then((data) => {
          this.services = data; 
        })
        .catch((error) => {
          console.error('Error fetching services:', error);
        });
    },
    async fetchLiveRequests() {
      try {
        const response = await fetch('http://localhost:5000/admin_dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json(); 
        this.liveRequests = data[0]; 
        this.inactiveUsers = data[1]; 
      } catch (error) {
        console.error('Error fetching live requests:', error);
      }
    },
    async removeUser(userId) {
      try {
        const response = await fetch('http://localhost:5000/delete_user', {
          method: 'POST', 
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
          body: JSON.stringify({ id: userId }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json(); 
        console.log(result.message || 'User deleted successfully');
        

        
        this.fetchLiveRequests();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    formatDate(dateString) {
      return dateString.replace(/(:\d{2})\sGMT$/, '');
    },
  },
};
</script>
