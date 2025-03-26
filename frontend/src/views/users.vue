<template>
  <div>
    <AdminNav />

    <div class="container mt-4">
      <div class="row">
        <div class="col-md-12">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <a class="navbar-brand text-primary fw-bold text-decoration-none me-2" href="/users">
              View All Users
            </a>
            <form @submit.prevent="searchUser" class="d-flex flex-grow-1">
              <input class="form-control me-2 border-dark" type="search"
              placeholder="Find Customer by Name, Email, Location or Pincode and Professionals by Service Name"
              aria-label="Search" v-model="searchTerm" required />
              <button class="btn btn-outline-dark" type="submit">Search</button>
            </form>
            <button class="btn btn-outline-dark ms-2" @click="create_csv">Export CSV Data</button>
          </div>
        </div>





        <!-- Customers List -->
        <div class="col-md-6">
          <h4 class="text-center">Customers</h4>
          <ul class="list-group">
            <li v-for="customer in customers" :key="customer.id"
              class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <b>{{ customer.name }}</b>, <small>ID: {{ customer.id }}</small> |
                <small :class="customer.is_active ? 'text-success' : 'text-danger'">
                  {{ customer.is_active ? 'Active' : 'Inactive' }}
                </small>

              </div>

              <div>
                <router-link :to="`/customer_history/${customer.id}`" class="btn btn-info btn-sm me-4">Booking
                  History</router-link>
                <router-link :to="`/user_profile/${customer.id}`" class="btn btn-info btn-sm">Profile</router-link>
              </div>
            </li>
          </ul>
        </div>

        <!-- Professionals List -->
        <div class="col-md-6">
          <h4 class="text-center">Professionals</h4>
          <ul class="list-group">
            <li v-for="professional in professionals" :key="professional.id"
              class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <b>{{ professional.name }}</b>, <small>ID: {{ professional.id }}</small> |
                <small :class="professional.is_active ? 'text-success' : 'text-danger'">
                  {{ professional.is_active ? 'Active' : 'Inactive' }}
                </small>
                <br />
                <b>{{ professional.service }}</b>
                <br />
                
                <small>Pincode: {{ professional.pincode }}</small>, <small>Phone: {{ professional.phone }}</small>
              </div>

              <div>
                <router-link :to="`/professional_history/${professional.id}`" class="btn btn-info btn-sm me-4">Work
                  History</router-link>
                <router-link :to="`/user_profile/${professional.id}`" class="btn btn-info btn-sm">Profile</router-link>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import AdminNav from '@/views/admin_nav.vue'; // Import AdminNav component

export default {
  components: {
    AdminNav
  },
  data() {
    return {
      searchTerm: '',
      customers: [],
      professionals: []
    };
  },
  mounted() {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");
    if (!token || role !== "Admin") {
      this.$router.push('/');
    }
  },
  setup() {
    const searchTerm = ref('');
    const customers = ref([]);
    const professionals = ref([]);

    const fetchUsers = async () => {
      try {
        const response = await fetch('http://localhost:5000/users', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
          },
        });
        const data = await response.json();
        // console.log(data)

        // Assuming the data returned from the API matches the structure you provided
        customers.value = data[0];
        professionals.value = data[1];
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };



    const create_csv = async () => {
      const res = await fetch('http://localhost:5000/create-csv/User', {
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

    const searchUser = () => {
      // Perform search logic here, could involve an API call or filter the list
      // console.log('Searching for:', searchTerm.value);
      const term = searchTerm.value.toLocaleLowerCase();
      customers.value = customers.value.filter(
        (customer) =>
          customer.name.toLowerCase().includes(term) ||
          customer.email.toLowerCase().includes(term) ||
          customer.phone.toLowerCase().includes(term) ||
          customer.address.toLowerCase().includes(term) ||
          customer.pincode.toLowerCase().includes(term)
      );
      professionals.value = professionals.value.filter(
        (professional) =>
          professional.name.toLowerCase().includes(term) ||
          professional.email.toLowerCase().includes(term) ||
          professional.phone.toLowerCase().includes(term) ||
          professional.address.toLowerCase().includes(term) ||
          professional.service.toLowerCase().includes(term) ||
          professional.pincode.toLowerCase().includes(term)
      );
    };
    // console.log(professionals.value)

    // Fetch user data on component mount
    fetchUsers();

    return {
      searchTerm,
      customers,
      professionals,
      // avgRating,
      searchUser,
      create_csv
    };
  }
};
</script>
