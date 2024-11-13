<template>
  <div class="sponsor-signup">
    <h1>Sponsor Registration</h1>
    <form @submit.prevent="registerSponsor">
      <input type="text" v-model="name" placeholder="Name" required />
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <input type="email" v-model="email" placeholder="Email" required />
      <select v-model="industry" required>
        <option disabled value="">Select Industry</option>
        <option>Finance</option>
        <option>Healthcare</option>
        <option>Automotive</option>
      </select>
      <button type="submit">Register</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SponsorSignup',
  data() {
    return {
      name: '',
      username: '',
      password: '',
      email: '',
      industry: '',
      errorMessage: ''
    };
  },
  methods: {
    registerSponsor() {
      const data = {
        name: this.name,
        email: this.email,
        password: this.password,
        industry: this.industry
      };

      axios
        .post('http://127.0.0.1:5000/signup/sponsor', data)
        // eslint-disable-next-line
        .then(response => {
          alert('Sponsor registered successfully');
          this.$router.push('/');
        })
        .catch(error => {
          this.errorMessage = error.response.data.message || 'An error occurred';
        });
    }
  }
};
</script>

<style scoped>
.sponsor-signup {
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
}

form input, select {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.error-message {
  color: red;
}
</style>
