<template>
  <div class="edit-profile">
    <div class="header">
      <h1>Edit Profile</h1>
      <button class="button go-back" @click="goBack">Go Back</button>
    </div>
    <form @submit.prevent="updateProfile">
      <input type="text" v-model="name" placeholder="Name" required />
      <input type="number" v-model="followers" placeholder="Followers" required />
      <button type="submit" class="button">Save Changes</button>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditInfluencerProfile',
  data() {
    return {
      name: '',
      followers: '',
      successMessage: '',
      errorMessage: ''
    };
  },
  created() {
    this.fetchProfileData();
  },
  methods: {
    fetchProfileData() {
      const token = localStorage.getItem('authToken');
      axios
        .get('http://127.0.0.1:5000/influencer/profile', {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.name = response.data.name;
          this.followers = response.data.followers;
        })
        .catch(error => {
          console.error("Error fetching profile data:", error);
        });
    },
    updateProfile() {
      const token = localStorage.getItem('authToken');
      const data = {
        name: this.name,
        followers: this.followers
      };
      axios
        .put('http://127.0.0.1:5000/edit_influencer_profile', data, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.successMessage = response.data.message;
          this.errorMessage = '';
        })
        .catch(error => {
          this.errorMessage = error.response.data.error || "Failed to update profile.";
          this.successMessage = '';
        });
    },
    goBack() {
      this.$router.push({ name: 'InfluencerDashboard' });
    }
  }
};
</script>

<style scoped>
.edit-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.edit-profile h1 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.edit-profile button.go-back {
  background-color: #6c757d;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  font-weight: bold;
}

.edit-profile button.go-back:hover {
  background-color: #4b6e89;
}

.edit-profile form {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-top: 20px;
}

.edit-profile input[type="text"],
.edit-profile input[type="number"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  color: #333;
}

.edit-profile button.button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

.edit-profile button.button:hover {
  background-color: #0056b3;
}

.edit-profile .success-message {
  color: #28a745;
  font-weight: bold;
  margin-top: 15px;
  text-align: center;
}

.edit-profile .error-message {
  color: #e74c3c;
  font-weight: bold;
  margin-top: 15px;
  text-align: center;
}
</style>
