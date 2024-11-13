<template>
  <div class="influencer-signup">
    <h1>Influencer Registration</h1>
    <form @submit.prevent="registerInfluencer">
      <input type="text" v-model="name" placeholder="Name" required />
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <input type="email" v-model="email" placeholder="Email" required />
      <select v-model="industry" required>
        <option disabled value="">Select Industry</option>
        <option>Fashion</option>
        <option>Tech</option>
        <option>Fitness</option>
      </select>
      <div class="platforms">
        <label>
          <input type="radio" value="YouTube" v-model="platform" /> YouTube
        </label>
        <label>
          <input type="radio" value="Twitter" v-model="platform" /> Twitter
        </label>
        <label>
          <input type="radio" value="Instagram" v-model="platform" /> Instagram
        </label>
      </div>
      <input type="number" v-model="followers" placeholder="Followers" required />
      <button type="submit">Register</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfluencerSignup',
  data() {
    return {
      name: '',
      username: '',
      password: '',
      email: '',
      industry: '',
      platform: '',
      followers: null,
      errorMessage: ''
    };
  },
  methods: {
    registerInfluencer() {
      const data = {
        name: this.name,
        email: this.email,
        password: this.password,
        industry: this.industry,
        platform: this.platform,
        followers: this.followers
      };

      axios
        .post('http://127.0.0.1:5000/signup/influencer', data)
        // eslint-disable-next-line
        .then(response => {
          alert('Influencer registered successfully');
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
.influencer-signup {
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

.platforms label {
  margin-right: 10px;
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
