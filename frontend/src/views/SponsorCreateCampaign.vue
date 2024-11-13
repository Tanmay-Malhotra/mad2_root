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
/* Add your styling here */
</style>
