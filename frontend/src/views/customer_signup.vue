<template>
    <div>
        <!-- Navbar -->
        <Navbar />

        <!-- Customer Registration Form -->
        <div class="container mt-5">
            <h2 class="text-center fw-bold">Customer Registration</h2>

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
                        <input v-model="email" type="email" id="email" name="email" class="form-control" required />
                    </div>
                </div>

                <!-- Password Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="password" class="col-sm-2 col-form-label text-end">Password:</label>
                    <div class="col-sm-5">
                        <input v-model="password" type="password" id="password" name="password" class="form-control"
                            minlength="5" required />
                    </div>
                </div>

                <!-- Phone Input -->
                <div class="mb-3 row justify-content-center">
                    <label for="phone" class="col-sm-2 col-form-label text-end">Phone:</label>
                    <div class="col-sm-5">
                        <input v-model="phone" type="tel" id="phone" name="phone" class="form-control"
                            pattern="[0-9]{10}" required />
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
                            pattern="[0-9]{6}" required />
                    </div>
                </div>

                <!-- Submit Button -->
                <div class="text-center">
                    <button type="submit" class="btn btn-primary">Register</button>
                </div>
            </form>

            <!-- Login Link -->
            <div class="mt-3 text-center">
                Already have a customer account? <router-link to="/customer_login">Log in</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from './nav.vue'; // Ensure correct path for Navbar component

export default {
    name: 'CustomerSignup', // Component name
    components: {
        Navbar // Include Navbar as a child component
    },
    data() {
        return {
            name: '',
            email: '',
            password: '',
            phone: '',
            address: '',
            pincode: ''
        };
    },
    methods: {
        handleSubmit() {
            // Construct the form data object
            const formData = {
                name: this.name,
                email: this.email,
                password: this.password,
                phone: this.phone,
                address: this.address,
                pincode: this.pincode,
            };

            // Log form data for debugging
            console.log('Form Data:', formData);

            // Make a POST request using fetch
            fetch('http://localhost:5000/customer_signup', {
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
                    this.$router.push('/');
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
/* Scoped styles for the component */
body {
    background-color: #f8f9fa;
    /* Matches bg-light class */
}
</style>