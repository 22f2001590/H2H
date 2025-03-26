<template>
  <div>
    <!-- Professional Navigation Component -->
    <ProfessionalNav />

    <div v-if="user.is_active" class="container mt-3">
      <div class="row">
        <div class="col-md-9">
          <div class="row mb-3">
            <div class="col-md-12 d-flex justify-content-between align-items-center">
              <h4 class="mb-0">All "{{ user.service }}" Live Requests</h4>
            </div>
          </div>
          <div class="container mt-4">
            <div class="row">
              <div class="col-12">
                <div class="list-group">
                  <div v-for="(rs, index) in requestedServices" :key="rs.id"
                    class="list-group-item p-4 mb-3 border-0 shadow-sm">
                    <div class="row align-items-center">
                      <div class="col-md-8">
                        <h5 class="mb-1">{{ rs.customer.address }}, {{ rs.customer.pincode }}</h5>
                        <p class="mb-0">
                          <strong>Requirements:</strong> {{ rs.requirement_message }}<br />
                          <strong>Date:</strong> {{ formatDate(rs.needed_at) }} IST
                        </p>
                      </div>
                      <div class="col-md-4 text-md-end mt-3 mt-md-0">
                        <a class="btn btn-success" @click="acceptRequest(rs.id)">Accept</a>

                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="row mb-3">
            <div class="col-md-12 d-flex justify-content-between align-items-center">
              <h4 class="mb-0">Upcoming Tasks</h4>
            </div>
          </div>
          <div class="container my-4">
            <div class="row">
              <div class="col-12">
                <div class="list-group">
                  <div v-for="(as, index) in acceptedServices" :key="as.id"
                    class="list-group-item p-4 mb-3 border-0 shadow-sm rounded-3">
                    <div class="row">
                      <!-- Details Section -->
                      <div class="col-12">
                        <p class="mb-0 text-muted">
                          <span class="fw-bold text-dark">Date:</span> {{ formatDate(as.needed_at) }} IST<br />
                          <!-- <span class="fw-bold text-dark">Time:</span> {{ formatTime(as.needed_at) }}<br /> -->
                          <span class="fw-bold text-dark">Name:</span> {{ as.customer.name }}<br />
                          <span class="fw-bold text-dark">Phone:</span> {{ as.customer.phone }}<br />
                          <span class="fw-bold text-dark">Address:</span> {{ as.customer.address }}<br />
                          <span class="fw-bold text-dark">Pincode:</span> {{ as.customer.pincode }}
                        </p>
                      </div>
                    </div>
                    <!-- Buttons Section -->
                    <div class="row mt-3">
                      <div class="col-12 text-center">
                        <div v-if="as.status === 'accepted'">
                          <button class="btn btn-danger px-4 py-2" @click="rejectRequest(as.id)">
                            Reject
                          </button>
                        </div>
                        <div v-else-if="as.status === 'paid'">
                          <button type="button" class="btn btn-success px-4 py-2" data-bs-toggle="modal"
                            :data-bs-target="'#closeModal-' + index">
                            Close
                          </button>
                          <div class="modal fade" :id="'closeModal-' + index" tabindex="-1"
                            :aria-labelledby="'modalLabel-' + index" aria-hidden="true">
                            <div class="modal-dialog">
                              <div class="modal-content">
                                <div class="modal-header d-flex flex-column align-items-start bg-light p-4">
                                  <div class="d-flex w-100 justify-content-between align-items-center">
                                    <div class="mt-3">
                                      <h1 class="modal-title fs-5 fw-bold" :id="'modalLabel-' + index">
                                        Confirm Payemnt
                                      </h1>
                                    </div>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                      aria-label="Close"></button>
                                  </div>

                                </div>

                                <div class="modal-body text-center">

                                  <form @submit.prevent="closeServiceRequest(as.id)">
                                    <!-- <input type="hidden" :value="lr.service.id" /> -->

                                    <div class="mb-3">
                                      <label class="form-label">Feedback Message</label>
                                      <textarea v-model="professionalFeedback" class="form-control" rows="4"
                                        required></textarea>
                                    </div>


                                    <button type="submit" class="btn btn-success">Close Now</button>
                                  </form>


                                </div>

                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <div v-else>
      <h1>Your account is not active. Please contact Admin.</h1>
    </div>
  </div>
</template>

<script>
import ProfessionalNav from "./professional_nav.vue"; // Import the navigation component

export default {
  components: {
    ProfessionalNav,
  },
  data() {
    return {
      professionalFeedback: "",
      user: {
        id: "", // Replace with actual user ID
        name: "", // Replace with actual user name
        service: "",
        service_id: "",
        is_active: false
      },
      requestedServices: [],
      acceptedServices: [],
    };
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (!token || role !== "Professional") {
      this.$router.push('/');
    }
    // Fetch user data when the component is mounted
    const user = JSON.parse(localStorage.getItem('user'))
    this.user.id = user.id;
    this.user.name = user.name;
    this.user.service = user.service;
    this.user.is_active = user.is_active;

    // Fetch requested services when the component is mounted
    this.fetchRequestedServices();
  },
  methods: {
    async fetchRequestedServices() {
      try {
        // Send GET request to the API endpoint
        const response = await fetch(`http://localhost:5000/professional_dashboard`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({ "id": this.user.id }),
        });

        // Parse the response as JSON
        const data = await response.json();

        // Store the requested services in the data property
        this.requestedServices = data[0];
        this.acceptedServices = data[1];
        // console.log(data);
      } catch (error) {
        console.error(error);
      }
    },
    async acceptRequest(serviceRequestId) {
      try {
        const response = await fetch(`http://localhost:5000/accept_request`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            service_request_id: serviceRequestId,
            professional_id: this.user.id, // Replace with the actual professional ID
          }),
        });

        if (!response.ok) {
          const error = await response.json();
          console.error('Error:', error);
          alert(`Failed to accept request: ${error.error}`);
          return;
        }

        const result = await response.json();

        // console.log('Request accepted:', result);
        // alert('Request successfully accepted!');
        this.fetchRequestedServices();
      } catch (err) {
        console.error('Fetch error:', err);
        // alert('An error occurred while accepting the request.');
      }

    },
    async rejectRequest(serviceRequestId) {
      try {
        const response = await fetch(`http://localhost:5000/reject_request`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            service_request_id: serviceRequestId,
            professional_id: this.user.id, // Replace with the actual professional ID
          }),
        });

        if (!response.ok) {
          const error = await response.json();
          console.error('Error:', error);
          alert(`Failed to accept request: ${error.error}`);
          return;
        }

        const result = await response.json();

        console.log('Request accepted:', result);
        // alert('Request successfully accepted!');
        this.fetchRequestedServices();
        // refresh this page
        this.$router.go();
      } catch (err) {
        console.error('Fetch error:', err);
        // alert('An error occurred while accepting the request.');
      }

    },
    async closeServiceRequest(serviceRequestId) {
      // console.log(serviceRequestId);
      // console.log(this.professionalFeedback);
      // return;
      try {
        const response = await fetch(`http://localhost:5000/close_request`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            service_request_id: serviceRequestId,
            feedback: this.professionalFeedback,
          }),
        });

        if (!response.ok) {
          const error = await response.json();
          console.error('Error:', error);
          // alert(`Failed to close request: ${error.error}`);
          return;
        }

        const result = await response.json();

        console.log('Request closed:', result);
        // alert('Request successfully closed!');
        this.fetchRequestedServices();
        this.$router.go();
        // this.fetchAcceptedServices();
      } catch (err) {
        console.error('Fetch error:', err);
        // alert('An error occurred while closing the request.');
      }
    },
    formatDate(dateString) {
      return dateString.replace(/(:\d{2})\sGMT$/, '');
    },
    
  },
};
</script>
