<template>
    <div>
      <!-- Navigation Bar -->
      <CustomerNav />
  
      <div class="container mt-4">
        <div class="row">
          <div class="col-md-12">
            <!-- Header Section -->
            <div class="row mb-3">
              <div class="col d-flex justify-content-between align-items-center">
                <h3 class="mb-0">Found {{ services.length }} Related Results</h3>
                <router-link to="/customer_dashboard" class="btn btn-primary">View All</router-link>
              </div>
            </div>
  
            <!-- Services List -->
            <div class="list-group">
              <div
                v-for="(service, index) in services"
                :key="service.id"
                class="list-group-item p-3 border rounded mb-3"
              >
                <h4 class="mb-2">{{ service.name }}</h4>
                <p class="text-muted">{{ service.description }}</p>
                <p>
                  <strong>Available in (pincode):</strong>
                  {{ service.users.map(user => user.pincode).join(", ") }}
                </p>
  
                <!-- Book Now Button -->
                <button
                  type="button"
                  class="btn btn-primary"
                  data-bs-toggle="modal"
                  :data-bs-target="`#book_now_modal-${index}`"
                >
                  Book Now
                </button>
  
                <!-- Modal -->
                <div
                  class="modal fade"
                  :id="`book_now_modal-${index}`"
                  tabindex="-1"
                  :aria-labelledby="`modalLabel-${index}`"
                  aria-hidden="true"
                >
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h1 class="modal-title fs-5" :id="`modalLabel-${index}`">
                          {{ service.name }}
                        </h1>
                        <button
                          type="button"
                          class="btn-close"
                          data-bs-dismiss="modal"
                          aria-label="Close"
                        ></button>
                      </div>
                      <div class="modal-body">
                        <form @submit.prevent="submitBooking(service.id)">
                          <div class="mb-3">
                            <label for="date" class="form-label">Select Date</label>
                            <input
                              type="date"
                              id="date"
                              v-model="booking.date"
                              class="form-control"
                              :min="currentDate"
                              required
                            />
                          </div>
                          <div class="mb-3">
                            <label for="time" class="form-label">Select Time</label>
                            <input
                              type="time"
                              id="time"
                              v-model="booking.time"
                              class="form-control"
                              required
                            />
                          </div>
                          <div class="mb-3">
                            <label for="requirement_message" class="form-label">
                              Any Specific Requirements
                            </label>
                            <textarea
                              id="requirement_message"
                              v-model="booking.requirementMessage"
                              class="form-control"
                              rows="4"
                              required
                            ></textarea>
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
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import CustomerNav from "./customer_nav.vue"; // Import the navigation component
  
  export default {
    components: {
      CustomerNav,
    },
    data() {
      return {
        services: [
          // Example service data, replace with actual API data
          {
            id: 1,
            name: "Plumbing Service",
            description: "Expert plumbing solutions for your home.",
            users: [{ pincode: "110001" }, { pincode: "110002" }],
          },
          {
            id: 2,
            name: "Electrical Service",
            description: "Reliable electrical repairs and installations.",
            users: [{ pincode: "110003" }, { pincode: "110004" }],
          },
        ],
        booking: {
          date: "",
          time: "",
          requirementMessage: "",
        },
        currentDate: new Date().toISOString().split("T")[0], // Get today's date
      };
    },
    methods: {
      submitBooking(serviceId) {
        // Mock submission logic
        console.log("Booking Submitted:", {
          serviceId,
          ...this.booking,
        });
        alert("Booking successfully submitted!");
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add necessary custom styles */
  </style>
  