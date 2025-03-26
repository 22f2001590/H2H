<template>
  <div>
    <!-- Customer Navbar -->
    <CustomerNav />

    <div v-if="user.isActive" class="container mt-3">
      <div class="row">
        <!-- Services Section -->
        <div class="col-md-9">
          <div class="row mb-3">
            <div class="col-md-12">
              <div class="d-flex justify-content-between align-items-center">
                <h4 class="mb-0">
                  <a class="navbar-brand text-primary fw-bold text-decoration-none" href="/customer_dashboard">
                    View All Services
                  </a>
                </h4>
                <form @submit.prevent="searchServices" class="d-flex flex-grow-1 ms-3">
                  <input class="form-control me-2 border-dark" type="search" v-model="searchTerm"
                    placeholder="Find Services or Search by Pincode | View All Services" aria-label="Search" required />
                  <button class="btn btn-outline-dark" type="submit">Search</button>
                </form>
              </div>
            </div>
          </div>

          <div class="list-group">
            <div v-for="(service, index) in services" :key="service.id" class="list-group-item">
              <h4 class="mb-2">{{ service.name }}</h4>
              <p class="text-muted">{{ service.description }} <br>
              </p>
              <p>
                <strong>Available in (pincode):</strong>
                {{ service.users.map(user => user.pincode).join(", ") }}
              </p>
              <div class="d-flex align-items-center justify-content-between text-muted">
                <span>
                  ₹{{ service.price }} for {{ service.time_required }} hrs
                </span>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                  :data-bs-target="'#bookNowModal-' + index">
                  --- Book Now >>>
                </button>
              </div>



              <!-- Book Now Modal -->
              <div class="modal fade" :id="'bookNowModal-' + index" tabindex="-1"
                :aria-labelledby="'modalLabel-' + index" aria-hidden="true">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" :id="'modalLabel-' + index">
                        {{ service.name }}
                      </h1>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                      <form @submit.prevent="bookService(service.id)">
                        <div class="mb-3">
                          <label for="date" class="form-label">Select Date</label>
                          <input type="date" id="date" v-model="booking.date" class="form-control" :min="currentDate"
                            required />
                        </div>
                        <div class="mb-3">
                          <label for="time" class="form-label">Select Time</label>
                          <input type="time" id="time" v-model="booking.time" class="form-control" required />
                        </div>
                        <div class="mb-3">
                          <label for="requirementMessage" class="form-label">Your Specific Requirements</label>
                          <textarea id="requirementMessage" v-model="booking.requirementMessage" class="form-control"
                            rows="4" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Live Requests Section -->
        <div class="col-md-3">
          <!-- Header Section -->
          <div class="col-md-12 d-flex justify-content-between align-items-center">
            <h4 class="text-center mb-4">Your Live Requests</h4>
          </div>

          <!-- Live Requests List -->
          <div class="list-group">
            <div v-for="(lr, index) in liveRequests" :key="lr.id" class="list-group-item">
              <!-- Service Name -->
              <h5>{{ lr.service.name }}</h5>

              <!-- Date and Time -->
              <h6>{{ formatDate(lr.needed_at) }} IST</h6>

              <!-- Status -->
              <p><span><b>Message: </b> {{ lr.requirement_message }}</span> <br>
                <b>Status:</b>
                <span v-if="lr.status === 'requested'" class="text-danger">
                  Service Professional Assignment Pending
                </span>
                <span v-else-if="lr.status === 'accepted'" class="text-success">
                  Assigned Service Professional
                </span><br>
              </p>


              <div class="d-flex justify-content-between align-items-center text-center">
                <button v-if="lr.status === 'accepted'" type="button" class="btn btn-primary" data-bs-toggle="modal"
                  :data-bs-target="'#payModal-' + index">
                  Pay
                </button>
                <button v-else type="button" class="btn btn-primary" data-bs-toggle="modal"
                  :data-bs-target="'#editRequest-' + index">
                  Edit
                </button>
                <div class="modal fade" :id="'editRequest-' + index" tabindex="-1"
                  :aria-labelledby="'modalLabel-' + index" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header d-flex flex-column align-items-start bg-light p-4">
                        <div class="d-flex w-100 justify-content-between align-items-center">
                          <div class="mt-3 text-left">
                            <h1 class="modal-title fs-5 fw-bold" :id="'modalLabel-' + index">
                              {{ lr.service.name }}
                            </h1>
                            <p class="mb-0 text-muted">
                              <strong>Date:</strong> {{ formatDate(lr.needed_at) }} IST<br>
                              <strong>Requirements:</strong> {{ lr.requirement_message }}
                            </p>
                          </div>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>

                      </div>

                      <div class="modal-body text-center">

                        <form @submit.prevent="editServiceRequest(lr.id, lr.service.id)">
                          <div class="mb-3">
                            <label for="date" class="form-label">Select Date</label>
                            <input type="date" id="date" v-model="booking.date" class="form-control" :min="currentDate"
                              required />
                          </div>
                          <div class="mb-3">
                            <label for="time" class="form-label">Select Time</label>
                            <input type="time" id="time" v-model="booking.time" class="form-control" required />
                          </div>
                          <div class="mb-3">
                            <label for="requirementMessage" class="form-label">Your Specific Requirements</label>
                            <textarea id="requirementMessage" v-model="booking.requirementMessage" class="form-control"
                              rows="4" required></textarea>
                          </div>
                          <button type="submit" class="btn btn-primary">Submit</button>
                        </form>

                      </div>

                    </div>
                  </div>
                </div>


                <div class="modal fade" :id="'payModal-' + index" tabindex="-1" :aria-labelledby="'modalLabel-' + index"
                  aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header d-flex flex-column align-items-start bg-light p-4">
                        <div class="d-flex w-100 justify-content-between align-items-center">
                          <div class="mt-3">
                            <h1 class="modal-title fs-5 fw-bold" :id="'modalLabel-' + index">
                              {{ lr.service.name }} Feedback
                            </h1>
                          </div>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>

                      </div>

                      <div class="modal-body text-center">

                        <form @submit.prevent="payServiceRequest(lr.id, lr.service.id)">
                          <input type="hidden" :value="lr.service.id" />

                          <div class="mb-3">
                            <label class="form-label">Feedback Message</label>
                            <textarea v-model="customerFeedback" class="form-control" rows="4" required></textarea>
                          </div>

                          <div class="mb-3">
                            <label class="form-label">Rating</label>
                            <select v-model="selectedRating" class="form-select" required>
                              <option value="" disabled>Select a rating among 1 to 5</option>
                              <option v-for="rating in [1, 2, 3, 4, 5]" :key="rating" :value="rating">
                                {{ rating }}
                              </option>
                            </select>
                          </div>


                          <button type="submit" class="btn btn-primary">Pay Now</button>
                        </form>


                      </div>

                    </div>
                  </div>
                </div>

                <!-- Cancel Button (If not accepted) -->
                <a v-if="lr.status !== 'accepted'" @click="cancelRequest(lr.id)" class="btn btn-danger"
                  href="javascript:void(0)">Cancel</a>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
    <div v-else>
      <h1>Your account is not active, Please contact Admin</h1>
    </div>
  </div>
</template>

<script>
import CustomerNav from "@/views/customer_nav.vue";

export default {
  components: { CustomerNav },
  data() {
    return {
      selectedRating: "",
      customerFeedback: "",
      user: { isActive: true }, 
      services: [],
      liveRequests: [], 
      searchTerm: "",
      currentDate: new Date().toISOString().split("T")[0],
      booking: {
        date: "",
        time: "",
        requirementMessage: "",
      },
      editbooking: {
        date: "",
        time: "",
        requirementMessage: "",
      },
    };
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (!token || role!=="Customer") {
      this.$router.push('/');
    }
    this.fetchServices();
    this.fetchLiveRequests();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch('http://localhost:5000/services', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch services');
        }
        this.services = await response.json();
       
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async fetchLiveRequests() {
      try {
        const userId = JSON.parse(localStorage.getItem("user")).id;  

        const response = await fetch('http://localhost:5000/live_requests', {
          method: 'POST',  
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
          body: JSON.stringify({
            user_id: JSON.parse(localStorage.getItem("user")).id  
          })
        });
        if (!response.ok) {
          throw new Error('Failed to fetch live requests');
        }
        this.liveRequests = await response.json();
        
      } catch (error) {
        console.error("Error fetching live requests:", error);
      }
    },
    async payServiceRequest(lr_id, lr_service_id) {
      try {
        const userId = JSON.parse(localStorage.getItem("user")).id;
        const response = await fetch(`http://localhost:5000/pay_request`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
          body: JSON.stringify({
            service_request_id: lr_id,
            feedback: this.customerFeedback,
            rating: this.selectedRating
          })
        });

        if (response.ok) {
          this.fetchLiveRequests()
          // refresh the current page
          this.$router.go();
        } else {
          // Handle failure (e.g., backend errors)
          const errorData = await response.json();
          console.log(`Error: ${errorData.message}`);
        }
      } catch (error) {
        console.error('Error:', error);
        
      }
    },
    searchServices() {
      
      const term = this.searchTerm.toLocaleLowerCase();
      
      this.services = this.services.filter(
        (service) =>
          service.name.toLowerCase().includes(term) ||
          service.description.toLowerCase().includes(term) ||
          service.users.some((user) => user.pincode.toLowerCase().includes(term))
      );

    },
    bookService(serviceId) {
      
      const userId = JSON.parse(localStorage.getItem("user")).id;

      // Prepare the data to send
      const bookingData = {
        service_id: serviceId,
        customer_id: userId,
        date: this.booking.date,
        time: this.booking.time,
        requirement_message: this.booking.requirementMessage
      };
      console.log(bookingData)
      
      fetch('http://localhost:5000/book_now', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
        body: JSON.stringify(bookingData)  
      })
        .then(response => response.json())  
        .then(data => {
          console.log("Booking successful:", data);  
          // refresh the current page
          this.$router.go();

        })
        .catch(error => {
          console.error("Error booking service:", error);  // Log any errors
        });
    },
    editServiceRequest(lrId, serviceId) {
      const userId = JSON.parse(localStorage.getItem("user")).id;

      
      const bookingData = {
        service_id: serviceId,
        customer_id: userId,
        date: this.booking.date,
        time: this.booking.time,
        requirement_message: this.booking.requirementMessage
      };
      console.log(bookingData)
      fetch(`http://localhost:5000/edit_request/${lrId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
        body: JSON.stringify(bookingData) 
      })
        .then(response => response.json())  
        .then(data => {
          console.log("Booking successful:", data); 
          // refresh the current page
          this.$router.go();
          

        })
        .catch(error => {
          console.error("Error booking service:", error);  
        });
    },
    async cancelRequest(requestId) {
      try {
        const response = await fetch(`http://localhost:5000/cancel_request/${requestId}`, {
          method: 'DELETE',  
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
        });

        if (response.ok) {
          this.fetchLiveRequests()
        } else {
          // Handle failure (e.g., backend errors)
          const errorData = await response.json();
          alert(`Error: ${errorData.message}`);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while canceling the request.');
      }
    },
    formatDate(dateString) {
      return dateString.replace(/(:\d{2})\sGMT$/, '');
    },
    formatDateForInput(dateString) {
      const date = new Date(dateString);
      return date.toISOString().split('T')[0];
    },
    formatTimeForInput(dateString) {
      const timePart = dateString.split(' ')[4]; 
      return timePart.slice(0, 5);
    },
  },
};
</script>
