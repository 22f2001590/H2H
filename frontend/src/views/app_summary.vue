<template>
  <div>
    <!-- Navbar -->
    <AdminNav />

    <div class="container mt-4">
      <div class="row">
        <div class="col-md-6">
          <div class="row mb-3">
            <div class="col-md-12 d-flex justify-content-between align-items-center">
              <h4 class="mb-0 text-center flex-grow-1">Service Requests</h4>
              <button class="btn btn-outline-dark" @click="create_csv">Export CSV Data</button>

            </div>

          </div>

          <div class="list-group">
            <div v-for="(lr, index) in serviceRequests" :key="lr.id" class="list-group-item p-3 mb-3 shadow-sm rounded">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div>
                  <h5 class="mb-0">{{ lr.service.name }}</h5>
                  <small class="text-muted">Service Request ID: {{ lr.id }}</small>
                </div>
                <div class="text-end">
                  <small class="text-muted">
                    Scheduled at:
                    {{ formatDate(lr.needed_at) }} IST
                  </small>
                </div>
              </div>

              <p class="mb-1">
                Status:
                <span v-if="lr.status === 'requested'" class="text-danger">Requested</span>
                <span v-else-if="lr.status === 'accepted'">
                  <span class="text-danger">Requested</span>,
                  <span class="text-warning">Accepted</span>
                </span>
                <span v-else-if="lr.status === 'paid'">
                  <span class="text-danger">Requested</span>,
                  <span class="text-warning">Accepted</span>,
                  <span class="text-success">Amount Paid</span>
                </span>
                <span v-else-if="lr.status === 'closed'">
                  <span class="text-danger">Requested</span>,
                  <span class="text-warning">Accepted</span>,
                  <span class="text-success">Amount Paid</span>,
                  <span class="text-dead">Request Closed</span>
                </span>
              </p>


              <div class="d-flex flex-column">
                <small class="d-flex">
                  <span class="fw-bold me-1">Customer Name:</span>
                  <span>{{ lr.customer.name }}</span>
                </small>
                <small class="d-flex">
                  <span class="fw-bold me-1">Requirement:</span>
                  <span>{{ lr.requirement_message }}</span>
                </small>

                <small v-if="lr.customer" class="d-flex">
                  <span class="fw-bold me-1">Customer Feedback:</span>
                  <span>{{ lr.customer_feedback }}</span>
                </small>
                <small v-if="lr.customer" class="d-flex">
                  <span class="fw-bold me-1">Customer Rating:</span>
                  <span>{{ lr.rating }}</span>
                </small>

                <small v-if="lr.professional" class="d-flex">
                  <span class="fw-bold me-1">Professional Name:</span>
                  <span>{{ lr.professional.name }}</span>
                </small>
                <small v-if="lr.professional" class="d-flex">
                  <span class="fw-bold me-1">Professional Feedback:</span>
                  <span>{{ lr.professional_feedback }}</span>
                </small>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="row mb-3">
            <div class="col-12 text-center">
              <h4 class="mb-0">Trending Services</h4>
            </div>
          </div>
          <div class="d-flex justify-content-center align-items-center">
            <img v-if="imageUrl" :src="imageUrl" alt="Service Requests Bar Graph" class="img-fluid"
              style="max-width: 100%; max-height: 100%; object-fit: contain;" />
            <p v-else>Loading image...</p>
          </div>
        </div>


      </div>
    </div>
  </div>
</template>

<script>
import AdminNav from "@/views/admin_nav.vue";

export default {
  components: {
    AdminNav,
  },
  data() {
    return {
      serviceRequests: [], 
      imageUrl: null,
    };
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (!token || role !== "Admin") {
      this.$router.push('/');
    }
    this.fetchHistory();
    this.fetchImage();
  },
  methods: {
    fetchImage() {

      // Fetch the image URL
      fetch('http://localhost:5000/image')
        .then((response) => {
          if (!response.ok) {
            throw new Error('Image fetch failed');
          }
          return response.blob(); // Convert response to Blob
        })
        .then((blob) => {
        
          this.imageUrl = URL.createObjectURL(blob);
        })
        .catch((error) => {
          console.error('Error fetching image:', error);
        });
    },
    async fetchHistory() {
      try {
        const response = await fetch('http://localhost:5000/app_summary', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': `Bearer ${localStorage.getItem("access_token")}`,
          },
        });


        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        this.serviceRequests = data;
      } catch (error) {
        console.error('Error fetching customer history:', error);
      }
    },
    async create_csv() {
      
      const res = await fetch('http://localhost:5000/create-csv/ServiceRequest', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      const task_id = (await res.json()).task_id
      console.log(task_id)

      const interval = setInterval(async () => {
        const res = await fetch(`http://localhost:5000/get-csv/${task_id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        if (res.ok) {
          console.log('data is ready')
          window.open(`http://localhost:5000/get-csv/${task_id}`)

          clearInterval(interval)
        }
      }, 100)
    },
    
    formatDate(dateString) {
      return dateString.replace(/(:\d{2})\sGMT$/, '');
    },
  },
};
</script>
