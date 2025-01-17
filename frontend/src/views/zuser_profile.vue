<template>
    
  
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
                  <strong>Service</strong>
                  <p>{{ user.service.name }} 
                    <a class="btn btn-outline-dark" :href="`/download/${user.doc_loc.split('\\').pop()}`" target="_blank">
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
              <p>{{ user.is_active ? 'Open' : 'Closed' }}</p>
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
                <button class="btn btn-warning" @click="showEditModal = true">Edit Details</button>
                <button class="btn btn-danger" @click="showDeleteModal = true">Remove Account</button>
              </div>
            </div>
            <div v-else>
              <a v-if="user.is_active" :href="`/user/flag/${user.id}`" class="btn btn-primary btn-sm w-50">
                Freeze User's Dashboard
              </a>
              <a v-else :href="`/user/flag/${user.id}`" class="btn btn-primary btn-sm w-50">
                Unfreeze User's Dashboard
              </a>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Edit Modal -->
      <div v-if="showEditModal" class="modal fade show" tabindex="-1">
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
      </div>
  
      <!-- Delete Modal -->
      <div v-if="showDeleteModal" class="modal fade show" tabindex="-1">
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
      </div>
    
  </template>
  
  <script>
  import { ref } from 'vue';
  import ProfessionalNav from './professional_nav.vue';
  import CustomerNav from './customer_nav.vue';
  import AdminNav from './admin_nav.vue';
  
  export default {
    components: {
      ProfessionalNav,
      CustomerNav,
      AdminNav
    },
    props: {
      user: Object,
      navUserRole: String
    },
    setup() {
      const showEditModal = ref(false);
      const showDeleteModal = ref(false);
      const editUser = ref({
        phone: user.phone,
        address: user.address,
        pincode: user.pincode
      });
  
      const updateUserDetails = () => {
        // Call API to update user details
        console.log(editUser.value);
        showEditModal.value = false;
      };
  
      const deleteUser = () => {
        // Call API to delete user account
        console.log('User deleted');
        showDeleteModal.value = false;
      };
  
      return {
        showEditModal,
        showDeleteModal,
        editUser,
        updateUserDetails,
        deleteUser
      };
    }
  };
  </script>
  
  <style scoped>
  /* Add custom styles if needed */
  </style>
  