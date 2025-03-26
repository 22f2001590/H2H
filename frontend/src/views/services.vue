<template>
  <div>
    <AdminNav />

    <div class="container mt-4">
      <div class="row">
        <!-- Service Management Section -->
        <div class="col-md-9">
          <!-- <div class="row mb-3"> -->
            <div class="d-flex justify-content-between align-items-center mb-3">
                <a class="navbar-brand text-primary fw-bold text-decoration-none me-2" href="/services">
                  View All Services
                </a>
              <form @submit.prevent="searchService" class="d-flex flex-grow-1">
                <input class="form-control me-2 border-dark" type="search"
                  placeholder="Find Services by Name or Description | View All Services" aria-label="Search"
                  v-model="searchTerm" required />
                <button class="btn btn-outline-dark" type="submit">Search</button>
              </form>
              <button class="btn btn-outline-dark ms-2" @click="create_csv">Export CSV Data</button>
            </div>
          <!-- </div> -->

          <ul class="list-group">
            <li v-for="service in services" :key="service.id" class="list-group-item">
              <div class="d-flex justify-content-between align-items-right">
                <div>
                  <span class="flex-shrink-0" style="width: 200px; white-space: nowrap;">
                    <b>{{ service.name }}</b> | {{ service.users.length }} professionals
                  </span>
                </div>

                <div>
                  <button type="button" class="btn btn-info btn-sm me-5" @click="showModal('view', service.id)">
                    Details
                  </button>

                  <button type="button" class="btn btn-warning btn-sm me-5" @click="showModal('edit', service.id)">
                    Edit
                  </button>

                  <button type="button" class="btn btn-danger btn-sm" @click="showModal('delete', service.id)">
                    Delete
                  </button>
                </div>
              </div>

              <!-- View Modal -->
              <div v-if="activeModal.type === 'view' && activeModal.id === service.id" class="modal fade show"
                style="display: block;" id="viewModal{{ service.id }}" tabindex="-1"
                aria-labelledby="viewModalLabel{{ service.id }}">
                <div class="modal-dialog modal-lg">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="viewModalLabel{{ service.id }}">Service Details</h1>
                      <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      <p><strong>Service ID:</strong> {{ service.id }}</p>
                      <p><strong>Service Name:</strong> {{ service.name }}</p>
                      <p><strong>Service Price:</strong> ₹{{ service.price }}</p>
                      <p><strong>Time Required (Hours):</strong> {{ service.time_required }}</p>
                      <p><strong>Service Description:</strong> {{ service.description }}</p>
                      
                    </div>
                  </div>
                </div>
              </div>

              <!-- Edit Modal -->
              <div v-if="activeModal.type === 'edit' && activeModal.id === service.id" class="modal fade show"
                style="display: block;" id="editModal{{ service.id }}" tabindex="-1"
                aria-labelledby="editModalLabel{{ service.id }}">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="editModalLabel{{ service.id }}">Edit Service</h1>
                      <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                      <form
                        @submit.prevent="editService(service.id, service.name, service.price, service.time_required, service.description)">
                        <div class="mb-3">
                          <label for="service_name{{ service.id }}" class="form-label">Service Name</label>
                          <input type="text" id="service_name{{ service.id }}" v-model="service.name"
                            name="service_name" class="form-control" required />
                        </div>
                        <div class="mb-3">
                          <label for="service_price{{ service.id }}" class="form-label">Service Price</label>
                          <input type="number" id="service_price{{ service.id }}" v-model="service.price"
                            name="service_price" class="form-control" required />
                        </div>
                        <div class="mb-3">
                          <label for="service_time{{ service.id }}" class="form-label">Time Required (Hours)</label>
                          <input type="number" id="service_time{{ service.id }}" v-model="service.time_required"
                            name="service_time" class="form-control" required />
                        </div>
                        <div class="mb-3">
                          <label for="service_description{{ service.id }}" class="form-label">Service
                            Description</label>
                          <textarea id="service_description{{ service.id }}" v-model="service.description"
                            name="service_description" class="form-control" rows="4" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Save changes</button>
                      </form>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Delete Modal -->
              <div v-if="activeModal.type === 'delete' && activeModal.id === service.id" class="modal fade show"
                style="display: block;" id="deleteModal{{ service.id }}" tabindex="-1"
                aria-labelledby="deleteModalLabel{{ service.id }}">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="deleteModalLabel{{ service.id }}">Confirm Delete</h1>
                      <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-left">
                      <p>Are you sure you want to delete the service <strong>{{ service.name }}</strong>?</p>

                      <form @submit.prevent="deleteService(service.id)" style="display:inline;">
                        <div class="text-center">
                          <button v-if="service.users.length === 0" type="submit" class="btn btn-danger">Delete</button>
                          <p v-if="service.users.length > 0">Cannot delete the service as it has associated
                            professionals.</p>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- New Service Creation -->
        <div class="col-md-3 text-center">
          <h4>New Service Creation</h4>
          <form @submit.prevent="createService">
            <div class="mb-3">
              <label for="service_name" class="form-label">Service Name</label>
              <input type="text" id="service_name" v-model="newService.name" name="service_name" class="form-control"
                required />
            </div>
            <div class="mb-3">
              <label for="service_price" class="form-label">Service Price</label>
              <input type="number" id="service_price" v-model="newService.price" name="service_price"
                class="form-control" value="" required />
            </div>
            <div class="mb-3">
              <label for="service_time" class="form-label">Time Required (Hours)</label>
              <input type="number" id="service_time" v-model="newService.time_required" name="service_time"
                class="form-control" value="" required />
            </div>
            <div class="mb-3">
              <label for="service_description" class="form-label">Service Description</label>
              <textarea id="service_description" v-model="newService.description" name="service_description"
                class="form-control" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Add Service</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import AdminNav from "./admin_nav.vue";

export default {
  components: {
    AdminNav
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (!token || role !== "Admin") {
      this.$router.push('/');
    }
  },
  setup() {
    const searchTerm = ref("");
    const services = ref([]);
    const newService = ref({
      name: '',
      price: null,
      time_required: null,
      description: '',
    });
    const activeModal = ref({
      type: "",
      id: null
    });

    const fetchServices = async () => {
      try {
        const response = await fetch('http://localhost:5000/services', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Include JWT token if required
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        services.value = data;
      } catch (error) {
        console.error('Failed to fetch services:', error);
      }
    };

  

    const showModal = (type, id) => {
      activeModal.value = { type, id };
    };

    const closeModal = () => {
      activeModal.value = { type: "", id: null };
    };

    const createService = async () => {
      try {
        const response = await fetch('http://localhost:5000/services', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: JSON.stringify(newService.value),
        });

        const result = await response.json();

        if (response.ok) {
          console.log(result.message);
          // Clear the form
          newService.value = {
            name: '',
            price: null,
            time_required: null,
            description: '',
          };
          fetchServices();
        } else {
          console.error(result.error);
        }
      } catch (error) {
        console.error('Error creating service:', error);
      }
    };

    const editService = async (id, sname, sprice, stime, sdesc) => {
      try {
        // Prepare the service data to be sent
        const updatedService = {
          name: sname,
          price: sprice,
          time_required: stime,
          description: sdesc,
        };
        // Send a PUT request to the backend
        const response = await fetch(`http://localhost:5000/services/edit/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Include JWT token if required
          },
          body: JSON.stringify(updatedService),
        });

        const result = await response.json();

        if (response.ok) {
          console.log(result.message);
          // Close the modal
          closeModal();
          // Optionally refetch the services to update the list
          fetchServices();
        } else {
          console.error(result.error);
          alert(result.error); // Show error message to the user
        }
      } catch (error) {
        console.error('Error editing service:', error);
        alert('An error occurred while updating the service.');
      }
      fetchServices();
    };

    const create_csv = async () => {
      // const token = this.getAuthToken() // Fetch token from local storage
      const res = await fetch('http://localhost:5000/create-csv/Service', {
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
          'Content-Type': 'application/json',
        })
        if (res.ok) {
          console.log('data is ready')
          window.open(`http://localhost:5000/get-csv/${task_id}`)

          clearInterval(interval)
        }
      }, 100)
    };

    const deleteService = async (id) => {
      try {
        const response = await fetch(`http://localhost:5000/services/delete/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Include JWT token if required
          },
        });

        const result = await response.json();

        if (response.ok) {
          console.log(result.message);
          // Optionally refresh or fetch the updated list of services
          fetchServices(); // Call a method to refresh the services list
        } else {
          console.error(result.error);
          alert(result.error); // Show error message to the user
        }
      } catch (error) {
        console.error('Error deleting service:', error);
        alert('An error occurred while deleting the service.');
      }
    };

    const searchService = () => {
      console.log("Searching for:", searchTerm.value);
      const term = searchTerm.value.toLocaleLowerCase();
      services.value = services.value.filter(
        (service) =>
          service.name.toLowerCase().includes(term) ||
          service.description.toLowerCase().includes(term)
      );

      console.log("Filtered services:", services.value);

    };

    // Fetch services when the component is mounted
    fetchServices();

    return {
      services,
      searchTerm,
      newService,
      activeModal,
      showModal,
      closeModal,
      createService,
      editService,
      deleteService,
      searchService,
      create_csv
    };
  }
};
</script>
