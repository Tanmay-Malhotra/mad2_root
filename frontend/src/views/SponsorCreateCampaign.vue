<template>
  <div class="create-campaign">
    <h1>Create New Campaign</h1>
    <form @submit.prevent="createCampaign">
      <input type="text" v-model="name" placeholder="Campaign Name" required />
      <select v-model="category" required>
        <option disabled value="">Select category</option>
        <option>Technology</option>
        <option>Finance</option>
        <option>Healthcare</option>
      </select>
      <input type="number" v-model="budget" placeholder="Budget" required />
      <input type="date" v-model="start_date" placeholder="Start Date" required />
      <input type="date" v-model="end_date" placeholder="End Date" />
      <button type="submit" class="button">Create Campaign</button>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateCampaign',
  data() {
    return {
      name: '',
      category: '',
      budget: '',
      start_date: '',
      end_date: '',
      successMessage: ''
    };
  },
  methods: {
  createCampaign() {
  const token = localStorage.getItem('authToken');
  console.log("Auth Token:", token);  // Debugging line
  const data = {
    name: this.name,
    category: this.category,
    budget: this.budget,
    start_date: this.start_date,
    end_date: this.end_date
  };
  axios
    .post('http://127.0.0.1:5000/sponsor/create_camp', data, {
      headers: { 'Authentication-Token': token }
    })
    .then(response => {
      this.successMessage = response.data.message;
      this.$router.push('/campaigns');
    })
    .catch(error => {
      console.error("Error creating campaign:", error);
    });
}

  }
};
</script>

<style scoped>
.create-campaign {
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

.create-campaign h1 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.create-campaign form {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.create-campaign input[type="text"],
.create-campaign select,
.create-campaign input[type="number"],
.create-campaign input[type="date"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  color: #333;
}

.create-campaign select {
  appearance: none;
}

.create-campaign button.button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
}

.create-campaign button.button:hover {
  background-color: #0056b3;
}

.create-campaign .success-message {
  color: #28a745;
  font-weight: bold;
  margin-top: 15px;
  text-align: center;
}
</style>

