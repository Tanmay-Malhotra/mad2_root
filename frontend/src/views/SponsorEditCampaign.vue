<template>
  <div class="edit-campaign">
    <h1>Edit Campaign</h1>
    <form @submit.prevent="updateCampaign">
      <input type="text" v-model="name" placeholder="Campaign Name" />
      <select v-model="category">
        <option disabled value="">Select category</option>
        <option>Technology</option>
        <option>Finance</option>
        <option>Healthcare</option>
      </select>
      <input type="number" v-model="budget" placeholder="Budget" />
      <input type="date" v-model="start_date" placeholder="Start Date" />
      <input type="date" v-model="end_date" placeholder="End Date" />
      <button type="submit" class="button">Update Campaign</button>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    </form>
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
        end_date: this.end_date
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
/* Add your styling here */
</style>
