<template>
  <div>
    <component :is="navComponent" />

    <div class="container mt-5">
      <div class="row">
        <div class="col-md-6 mx-auto">
          <h2 class="mb-4 text-center">User Profile</h2>

          <div class="mb-3">
            <strong>User Name</strong>
            <p>{{ user.name }}</p>
          </div>

          <div v-if="navUserRole === 'Admin' || navUserRole === 'Professional'">
            <div v-if="user.doc_loc">
              <div class="mb-3">
                <strong>Service Name</strong>
                <p>{{ user.service }}
                </p>
              </div>
              <div class="mb-3">
                <strong>Service Experience</strong>
                <p>
                  <a class="btn btn-outline-dark" :href="`${user.doc_loc}`" target="_blank">
                    View Experience PDF
                  </a>
                </p>
              </div>
            </div>
          </div>

          <div class="mb-3">
            <strong>Email</strong>
            <p>{{ user.email }}</p>
          </div>

          <div class="mb-3">
            <strong>Dashboard Access</strong>
            <p :class="user.is_active ? 'text-success' : 'text-danger'">
              {{ user.is_active ? 'Open' : 'Closed' }}
            </p>
          </div>


          <div class="mb-3">
            <strong>Phone</strong>
            <p>{{ user.phone }}</p>
          </div>

          <div class="mb-3">
            <strong>Address</strong>
            <p>{{ user.address }}</p>
          </div>

          <div class="mb-3">
            <strong>Pincode</strong>
            <p>{{ user.pincode }}</p>
          </div>

          <div v-if="navUserRole !== 'Admin'">
            <div class="d-flex justify-content-between">
              <!-- <button class="btn btn-warning" @click="showEditModal = true">Edit Details</button> -->
              <button type="button" class="btn btn-warning btn-sm me-5" @click="showModal('edit', user.id)">
                Edit Details
              </button>

              <div v-if="activeModal.type === 'edit' && activeModal.id === user.id" class="modal fade show"
                style="display: block;" id="editModal{{ user.id }}" tabindex="-1"
                aria-labelledby="editModalLabel{{ user.id }}">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="editModalLabel{{ user.id }}">Edit user</h1>
                      <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                      <form @submit.prevent="updateUser(user.id, user.phone, user.address, user.pincode)">
                        <div class="mb-3">
                          <label for="user_phone{{ user.id }}" class="form-label">Phone</label>
                          <input type="text" id="user_phone{{ user.id }}" v-model="user.phone" name="user_phone"
                            class="form-control" required />
                        </div>
                        <div class="mb-3">
                          <label for="user_address{{ user.id }}" class="form-label">Address</label>
                          <input type="text" id="user_address{{ user.id }}" v-model="user.address" name="user_address"
                            class="form-control" required />
                        </div>
                        <div class="mb-3">
                          <label for="user_pincode{{ user.id }}" class="form-label">Pincode</label>
                          <input type="text" id="user_pincode{{ user.id }}" v-model="user.pincode" name="user_pincode"
                            class="form-control" required />
                        </div>
                        <button type="submit" class="btn btn-primary">Save changes</button>
                      </form>
                    </div>
                  </div>
                </div>
              </div>





              <button type="button" class="btn btn-danger btn-sm" @click="showModal('delete', user.id)">
                Remove Account
              </button>
              <div v-if="activeModal.type === 'delete' && activeModal.id === user.id" class="modal fade show"
                style="display: block;" id="deleteModal{{ user.id }}" tabindex="-1"
                aria-labelledby="deleteModalLabel{{ user.id }}">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="deleteModalLabel{{ user.id }}">Confirm Delete</h1>
                      <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-left">
                      <p>Are you sure you want to delete your Account, <strong>{{ user.name }}</strong>?</p>

                      <form @submit.prevent="deleteUser" style="display:inline;">
                        <div class="text-center">
                          <button type="submit" class="btn btn-danger">Delete</button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <a v-if="user.is_active" @click="toggleUserStatus(user.id, 'freeze')" class="btn btn-primary btn-sm w-50">
              Freeze User's Dashboard
            </a>
            <a v-else @click="toggleUserStatus(user.id, 'unfreeze')" class="btn btn-primary btn-sm w-50">
              Unfreeze User's Dashboard
            </a>

          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <!-- <div v-if="showEditModal" class="modal fade show" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Your Details</h5>
            <button type="button" class="btn-close" @click="showEditModal = false"></button>
          </div>
          <div class="modal-body text-center">
            <form @submit.prevent="updateUserDetails">
              <div class="mb-3">
                <label for="user_phone" class="form-label">Phone</label>
                <input type="number" class="form-control" v-model="editUser.phone" required />
              </div>

              <div class="mb-3">
                <label for="user_address" class="form-label">Address</label>
                <textarea class="form-control" v-model="editUser.address" rows="3" required></textarea>
              </div>

              <div class="mb-3">
                <label for="user_pincode" class="form-label">Pincode</label>
                <input type="number" class="form-control" v-model="editUser.pincode" required />
              </div>

              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div> -->

    <!-- Delete Modal -->
    <!-- <div v-if="showDeleteModal" class="modal fade show" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-danger">Confirm Delete</h5>
            <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body text-center">
            <p>Are you sure you want to delete your account?</p>
            <form @submit.prevent="deleteUser">
              <div class="d-grid">
                <button type="submit" class="btn btn-danger">Delete My Account</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script>
import { ref } from 'vue';
import ProfessionalNav from './professional_nav.vue';
import CustomerNav from './customer_nav.vue';
import AdminNav from './admin_nav.vue';
import { useRouter } from 'vue-router';


export default {
  components: {
    ProfessionalNav,
    CustomerNav,
    AdminNav
  },
  data() {
    return {
      navUserRole: localStorage.getItem('role'),
      //   const activeModal: ref({
      //   type="",
      //   id=null
      // }),
    };
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");

    const userId = JSON.parse(localStorage.getItem("user")).id;  // Safely access userId
    const urlUserId = this.$route.params.id; // Assumes `id` is defined in the route parameters

    if (!token ||  (String(userId) !== urlUserId && role !== "Admin")) {
      this.$router.push('/');
    }
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
  // props: {
  //   navUserRole: String // Remove `user` prop since it will be fetched
  // },
  setup() {
    const user = ref({}); // Initialize user as null
    const showEditModal = ref(false);
    // const showDeleteModal = ref(false);
    const editUser = ref({
      phone: '',
      address: '',
      pincode: ''
    });
    const activeModal = ref({
      type: "",
      id: null
    });
    const showModal = (type, id) => {
      activeModal.value = { type, id };
    };
    const closeModal = () => {
      activeModal.value = { type: "", id: null };
    };

    // Function to fetch user data
    const fetchUser = async (id) => {
      try {
        const response = await fetch(`http://localhost:5000/user_profile/${id}`);
        if (!response.ok) {
          throw new Error(`Error fetching user: ${response.statusText}`);
        }
        const data = await response.json();
        user.value = data; // Assign fetched data to user
        // editUser.value = {
        //   phone: data.phone,
        //   address: data.address,
        //   pincode: data.pincode
        // };
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    };
    // async removeUser(userId) {
    //   try {
    //     const response = await fetch('http://localhost:5000/delete_user', {
    //       method: 'POST', // Change to POST for sending data
    //       headers: {
    //         'Content-Type': 'application/json',
    //       },
    //       body: JSON.stringify({ id: userId }),
    //     });

    //     if (!response.ok) {
    //       throw new Error(`HTTP error! status: ${response.status}`);
    //     }

    //     const result = await response.json(); // Assuming the API returns a JSON response
    //     console.log(result.message || 'User deleted successfully');
    //     // this.$router.go();

    //     // Optionally refresh data or update the UI
    //     this.fetchLiveRequests(); // If you're fetching a list of users, re-fetch them
    //   } catch (error) {
    //     console.error('Error deleting user:', error);
    //   }
    // };

    const toggleUserStatus = async (userId, action) => {
      const url = `http://localhost:5000/user/flag/${userId}`; // Construct the endpoint dynamically
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ action }) // Pass the action as payload
        });

        if (!response.ok) {
          throw new Error(`Error updating user status: ${response.statusText}`);
        }

        const result = await response.json();
        console.log(result);

        // Toggle `is_active` status after a successful request
        user.value.is_active = action === 'unfreeze';
      } catch (error) {
        console.error('Failed to update user status:', error);
      }
    };
    const updateUser = async (uid, uphone, uaddress, upincode) => {
      try {
        // Prepare the service data to be sent
        const updatedUser = {
          user_id: uid,
          phone: uphone,
          address: uaddress,
          pincode: upincode,
        };
        const response = await fetch(`http://localhost:5000/user/edit`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Include JWT token if required
          },
          body: JSON.stringify(updatedUser),
        });

        const result = await response.json();

        if (response.ok) {
          console.log(result.message);
          // Close the modal
          closeModal();
          // Optionally refetch the services to update the list
        } else {
          console.error(result.error);
          alert(result.error); // Show error message to the user
        }
      } catch (error) {
        console.error('Error editing service:', error);
        alert('An error occurred while updating the service.');
      }
      // fetchUser();
    };

    const deleteUser = async () => {
      const router = useRouter();
      try {
        const body = JSON.stringify({ id: user.value.id });
        const response = await fetch('http://localhost:5000/delete_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: body,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result.message || 'User deleted successfully');
        localStorage.clear();
        // router.push('/');
        window.location.href = '/';

      } catch (error) {
        console.error('Error deleting user:', error);
      }
    };

    const getUserIdFromUrl = () => {
      const path = window.location.pathname; // Get the current URL path
      const segments = path.split('/'); // Split the path into segments
      return segments[segments.length - 1]; // Get the last segment
    };

    // Extract user ID from the URL
    const userId = getUserIdFromUrl();
    fetchUser(userId);

    return {
      user,
      toggleUserStatus,
      showEditModal,
      // showDeleteModal,
      editUser,
      updateUser,
      deleteUser,
      activeModal,
      showModal,
      closeModal,
    };
  }
};

</script>

<!-- <style scoped>
.text-dead {
  color: gray;
}
</style> -->
