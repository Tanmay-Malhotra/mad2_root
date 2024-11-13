<template>
  <div class="login-page">
    <div class="login-container">
      <h1>Login @ SPOC</h1>
      <h2>Sponsor-Influencer Coordination</h2>
      <form @submit.prevent="signin_fn">
        <div class="form-group">
          <input type="email" v-model="email" placeholder="Email" required />
        </div>
        <div class="form-group">
          <input type="password" v-model="password" placeholder="Password" required />
        </div>
        <button class="login-button" type="submit">Login</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
      <p class="register-text">
        Is this your first time accessing SPOC? Register here:
      </p>
      <div class="register-buttons">
        <router-link to="/register-sponsor">
          <button class="register-button sponsor">Register as Sponsor</button>
        </router-link>
        <router-link to="/register-influencer">
          <button class="register-button influencer">Register as Influencer</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    signin_fn() {
      this.errorMessage = '';
      axios
        .post('http://127.0.0.1:5000/signin', {
          email: this.email,
          password: this.password
        })
        .then(response => {
          if (response.status === 200) {
            const token = response.data.authToken;
            const role = response.data.role;
            const sponsorId = response.data.sponsorId; // Capture sponsorId if available
            const influencerId = response.data.influencerId; // Capture influencerId if available

            // Store authToken in localStorage
            localStorage.setItem('authToken', token);

            // Store sponsorId if the user is a sponsor
            if (role === 'sponsor' && sponsorId) {
              localStorage.setItem('sponsorId', sponsorId);
            }

            // Store influencerId if the user is an influencer
            if (role === 'influencer' && influencerId) {
              localStorage.setItem('influencerId', influencerId);
            }

            // Redirect based on the role
            if (role === 'admin') {
              this.$router.push('/admin-dashboard');
            } else if (role === 'sponsor') {
              this.$router.push('/sponsor-dashboard');
            } else if (role === 'influencer') {
              this.$router.push('/influencer-dashboard');
            } else {
              this.errorMessage = 'Unknown user role. Please contact support.';
            }
          } else {
            this.errorMessage = 'Invalid email or password';
          }
        })
        // eslint-disable-next-line
        .catch(error => {
          this.errorMessage = 'Failed to log in. Please check your credentials.';
        });
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f4f4f4;
  font-family: 'Roboto', sans-serif;
}

.login-container {
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
  margin-bottom: 10px;
}

h2 {
  font-size: 18px;
  color: #555;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.login-button {
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

.login-button:hover {
  background-color: #3498db;
}

.register-text {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.register-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}

.register-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
}

.register-button.sponsor {
  background-color: #27ae60;
  color: white;
}

.register-button.influencer {
  background-color: #27ae60;
  color: white;
}

.register-button:hover {
  background-color: #2ecc71;
}

.error {
  color: #e74c3c;
  margin-top: 10px;
}
</style>
