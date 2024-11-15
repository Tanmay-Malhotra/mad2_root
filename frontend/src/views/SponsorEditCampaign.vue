<template>
  <div class="edit-campaign-container">
    <div class="edit-campaign-card">
      <h1>Edit Campaign</h1>
      <form @submit.prevent="updateCampaign">
        <label>Campaign Name:</label>
        <input type="text" v-model="name" placeholder="Enter campaign name" />

        <label>Category:</label>
        <select v-model="category">
          <option disabled value="">Select category</option>
          <option>Technology</option>
          <option>Finance</option>
          <option>Healthcare</option>
        </select>

        <label>Budget:</label>
        <input type="number" v-model="budget" placeholder="Enter budget" />

        <label>Start Date:</label>
        <input type="date" v-model="start_date" />

        <label>End Date:</label>
        <input type="date" v-model="end_date" />

        <label>Type:</label>
        <select v-model="type">
          <option disabled value="">Select type</option>
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>

        <button type="submit" class="button">Update Campaign</button>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditCampaign',
  props: ['campaignId'],
  data() {
    return {
      name: '',
      category: '',
      budget: '',
      start_date: '',
      end_date: '',
      type: '', // Add type data property
      successMessage: ''
    };
  },
  mounted() {
    this.fetchCampaignDetails();
  },
  methods: {
    fetchCampaignDetails() {
      const token = localStorage.getItem('authToken');
      axios
        .get(`http://127.0.0.1:5000/edit_campaign/${this.campaignId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          const campaign = response.data;
          this.name = campaign.name;
          this.category = campaign.category;
          this.budget = campaign.budget;
          this.start_date = campaign.start_date;
          this.end_date = campaign.end_date;
          this.type = campaign.type; // Set type data
        })
        .catch(error => {
          console.error("Error fetching campaign details:", error);
        });
    },
    updateCampaign() {
      const token = localStorage.getItem('authToken');
      const data = {
        name: this.name,
        category: this.category,
        budget: this.budget,
        start_date: this.start_date,
        end_date: this.end_date,
        type: this.type // Include type in update data
      };
      axios
        .put(`http://127.0.0.1:5000/edit_campaign/${this.campaignId}`, data, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.successMessage = response.data.message;
          this.$router.push('/campaigns');
        })
        .catch(error => {
          console.error("Error updating campaign:", error);
        });
    }
  }
};
</script>

<style scoped>
.edit-campaign-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f4;
}

.edit-campaign-card {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 100%;
}

.edit-campaign-card h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.edit-campaign-card form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.edit-campaign-card label {
  font-weight: bold;
}

.edit-campaign-card input,
.edit-campaign-card select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
}

.button:hover {
  background-color: #0056b3;
}

.success-message {
  color: green;
  text-align: center;
  font-weight: bold;
  margin-top: 10px;
}
</style>
