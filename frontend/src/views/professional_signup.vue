<template>
    <div>
        <!-- Navbar -->
        <Navbar />

        <!-- Professional Registration Form -->
        <div class="container mt-5">
            <h2 class="text-center fw-bold">Service Professional Registration</h2>

            <form @submit.prevent="handleSubmit" class="mt-4">
                <!-- Name Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="name" class="col-sm-2 col-form-label text-end">Name:</label>
                    <div class="col-sm-5">
                        <input v-model="name" type="text" id="name" name="name" class="form-control" required />
                    </div>
                </div>

                <!-- Email Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="email" class="col-sm-2 col-form-label text-end">Email:</label>
                    <div class="col-sm-5">
                        <input v-model="email" type="text" id="email" name="email" class="form-control" required />
                    </div>
                </div>

                <!-- Phone Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="phone" class="col-sm-2 col-form-label text-end">Phone:</label>
                    <div class="col-sm-5">
                        <input v-model="phone" type="text" id="phone" name="phone" class="form-control" required />
                    </div>
                </div>

                <!-- Address Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="address" class="col-sm-2 col-form-label text-end">Address:</label>
                    <div class="col-sm-5">
                        <input v-model="address" type="text" id="address" name="address" class="form-control"
                            required />
                    </div>
                </div>

                <!-- Pincode Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="pincode" class="col-sm-2 col-form-label text-end">Pincode:</label>
                    <div class="col-sm-5">
                        <input v-model="pincode" type="text" id="pincode" name="pincode" class="form-control"
                            required />
                    </div>
                </div>

                <!-- Service Select -->
                <div class="mb-3 row justify-content-center">
                    <label for="service" class="col-sm-2 col-form-label text-end">Select Service:</label>
                    <div class="col-sm-5">
                        <select v-model="service_id" name="service_id" id="service_id" class="form-select" required>
                            <option value="" disabled selected>Select a Service</option>
                            <option v-for="serviceOption in services" :key="serviceOption.id" :value="serviceOption.id">
                                {{ serviceOption.name }}
                            </option>
                            <option value="-1">Other (Please mention in the PDF)</option>
                        </select>
                    </div>
                </div>

                <!-- Work Experience Upload -->
                <div class="mb-3 row justify-content-center">
                    <label for="pincode" class="col-sm-2 col-form-label text-end">Google Drive link of your Work
                        Experience:</label>
                    <div class="col-sm-5">
                        <input v-model="doc_loc" type="text" id="doc_loc" name="doc_loc" class="form-control"
                            required />
                    </div>
                </div>

                <!-- Password Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="password" class="col-sm-2 col-form-label text-end">Password:</label>
                    <div class="col-sm-5">
                        <input v-model="password" type="password" id="password" name="password" class="form-control"
                            required />
                    </div>
                </div>

                <!-- Submit Button -->
                <div class="text-center">
                    <button type="submit" class="btn btn-primary">Register</button>
                </div>
            </form>

            <!-- Login Link -->
            <div class="mt-3 text-center">
                Already have a professional account? <router-link to="/professional_login">Log in</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from "./nav.vue"; // Ensure this path matches your project structure
export default {
    name: "ProfessionalSignup",
    components: {
        Navbar,
    },
    data() {
        return {
            services: [],
            name: '',
            email: '',
            phone: '',
            address: '',
            pincode: '',
            service_id: '',
            doc_loc: '',
            password: '',
        };
    },
    mounted(){
        this.fetchServices();
    },
    methods: {
        fetchServices() {
            fetch('http://localhost:5000/services')
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.json(); // Parse JSON response
                })
                .then((data) => {
                    this.services = data; // Assign fetched data to `services`
                })
                .catch((error) => {
                    console.error('Error fetching services:', error);
                });
        },
        handleSubmit() {
            // Construct the form data object
            const formData = {
                name: this.name,
                email: this.email,
                phone: this.phone,
                address: this.address,
                pincode: this.pincode,
                service_id: this.service_id,
                doc_loc: this.doc_loc,
                password: this.password,
            };

            // Log form data for debugging
            console.log('Form Data:', formData);

            // Make a POST request using fetch
            fetch('http://localhost:5000/professional_signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Specify the content type
                },
                body: JSON.stringify(formData), // Convert form data to JSON string
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.json(); // Parse the JSON response
                })
                .then((data) => {
                    console.log('Success:', data);
                    alert('Registration successful, Log in now!');
                    this.$router.push('/professional_login');
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('An error occurred while registering. Please try again.');
                });
        }
    }
};
</script>

<style scoped>
/* Scoped styles for this component */
body {
    background-color: #f8f9fa;
    /* Matches bg-light class */
}
</style>