<template>
  <div class="registration-page">
    <div class="registration-container">
      <h1>Sponsor Registration</h1>
      <form @submit.prevent="registerSponsor">
        <div class="form-group">
          <input type="text" v-model="name" placeholder="Name" required />
        </div>
        <div class="form-group">
          <input type="text" v-model="username" placeholder="Username" required />
        </div>
        <div class="form-group">
          <input type="password" v-model="password" placeholder="Password" required />
        </div>
        <div class="form-group">
          <input type="email" v-model="email" placeholder="Email" required />
        </div>
        <div class="form-group">
          <select v-model="industry" required>
            <option value="" disabled>Select Industry</option>
            <option value="Technology">Technology</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Finance">Finance</option>
            <option value="Education">Education</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <button class="register-button" type="submit">Register</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
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
      this.errorMessage = '';
      axios
        .post('http://localhost:5000/register-sponsor', {
          name: this.name,
          username: this.username,
          password: this.password,
          email: this.email,
          industry: this.industry
        })
        .then(response => {
          if (response.status === 200) {
            this.$router.push('/login'); // Redirect to login page on success
          } else {
            this.errorMessage = 'Registration failed. Please try again.';
          }
        })
        // eslint-disable-next-line
        .catch(error => {
          this.errorMessage = 'Registration failed. Please check your inputs and try again.';
        });
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.registration-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f4f4f4;
  font-family: 'Roboto', sans-serif;
}

.registration-container {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

h1 {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.register-button {
  width: 100%;
  padding: 10px;
  background-color: #2980b9;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.register-button:hover {
  background-color: #3498db;
}

.error {
  color: #e74c3c;
  margin-top: 10px;
}
</style>
