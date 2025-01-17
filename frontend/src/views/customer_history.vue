<template>
  <div>
    <component :is="navComponent" />

    <div class="container mt-4">
      <div class="row">
        <div class="col-md-12">
          <div class="row mb-3">
            <div class="col-md-12 d-flex justify-content-between align-items-center">
              <h4 class="mb-0 flex-grow-1 text-start">Service Requests</h4>
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
                  <span class="fw-bold me-1">Requirement:</span>
                  <span>{{ lr.requirement_message }}</span>
                </small>

                <small v-if="lr.customer_feedback" class="d-flex">
                  <span class="fw-bold me-1">Customer Feedback:</span>
                  <span>{{ lr.customer_feedback }}</span>
                </small>
                <small v-if="lr.customer_feedback" class="d-flex">
                  <span class="fw-bold me-1">Customer Rating:</span>
                  <span>{{ lr.rating }}</span>
                </small>

                <small v-if="lr.professional_feedback" class="d-flex">
                  <span class="fw-bold me-1">Professional Feedback:</span>
                  <span>{{ lr.professional_feedback }}</span>
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CustomerNav from '@/views/customer_nav.vue';
import ProfessionalNav from '@/views/professional_nav.vue';
import AdminNav from '@/views/admin_nav.vue';

export default {
  components: {
    CustomerNav,
    ProfessionalNav,
    AdminNav,
  },
  data() {
    return {
      serviceRequests: [], // You will populate this array from API or props
    };
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (!token || (role !== "Customer" && role !== "Admin")) {
      this.$router.push('/');
    }
    this.fetchCustomerHistory();
  },
  computed: {
    navComponent() {
      if (localStorage.getItem('role') === 'Customer') {
        return 'CustomerNav';
      } else if (localStorage.getItem('role') === 'Professional') {
        return 'ProfessionalNav';
      } else if (localStorage.getItem('role') === 'Admin') {
        return 'AdminNav';
      }
      return null;
    }
  },
  methods: {
    async create_csv() {
      // const token = this.getAuthToken() // Fetch token from local storage
      const res = await fetch(`http://localhost:5000/create-csv/customer/ServiceRequest/${this.$route.params.id}`, {
        method: 'GET',
        headers: {
          //   'Authentication-Token': token, // Add token in the headers
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
    async fetchCustomerHistory() {
      try {
        const response = await fetch('http://localhost:5000/customer_history', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id: this.$route.params.id }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        this.serviceRequests = data; // Assuming the API returns an array
      } catch (error) {
        console.error('Error fetching customer history:', error);
      }
    },
    formatDate(dateString) {
      return dateString.replace(/(:\d{2})\sGMT$/, '');
    },
  },
};
</script>

<style scoped>
.text-dead {
  color: gray;
}
</style>