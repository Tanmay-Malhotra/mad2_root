<template>
  <div>
    <!-- Navigation Bar -->
    <header>
      <div class="navbar-brand">Sponsor @ SPOC</div>
      <div class="user-actions">
        <router-link to="/sponsor-dashboard" class="nav-link">Profile</router-link>
        <router-link to="/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="/find-influencers" class="nav-link">Find</router-link>
        <button class="button logout" @click="logout">Logout</button>
      </div>
    </header>

    <!-- Content Section -->
    <div class="content">
      <div class="header">
        <h1>Your Campaigns</h1>
        <button @click="navigateToCreateCampaign" class="button create-button">Create New Campaign</button>
      </div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="campaigns.length">
        <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-card">
          <h3>{{ campaign.name }}</h3>
          <p>Status: {{ campaign.status }}</p>
          <p>Budget: {{ campaign.budget }}</p>
          <p>Category: {{ campaign.category }}</p>
          <p>Start Date: {{ campaign.start_date }}</p>
          <p>End Date: {{ campaign.end_date }}</p>
          <button @click="editCampaign(campaign.id)" class="button edit-button">Edit</button>
          <button @click="viewAdRequests(campaign.id)" class="button ad-requests-button">View Ad Requests</button>
          <button @click="deleteCampaign(campaign.id)" class="button delete-button">Delete</button>
        </div>
      </div>
      <div v-else>
        <p>No campaigns found. Create a new campaign to get started.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SponsorCampaigns',
  data() {
    return {
      campaigns: [],
      successMessage: ''
    };
  },
  mounted() {
    this.fetchCampaigns();
  },
  methods: {
    fetchCampaigns() {
      const sponsorId = localStorage.getItem('sponsorId');
      const token = localStorage.getItem('authToken');
      axios
        .get(`http://127.0.0.1:5000/campaigns/${sponsorId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          console.log('Fetched campaigns:', response.data.campaigns);
          this.campaigns = response.data.campaigns;
        })
        .catch(error => {
          console.error("Error fetching campaigns:", error);
        });
    },
    navigateToCreateCampaign() {
      this.$router.push('/create-campaign');
    },
    editCampaign(campaignId) {
      this.$router.push({ name: 'EditCampaign', params: { campaignId } });
    },
    viewAdRequests(campaignId) {
      this.$router.push({ name: 'ViewAdRequests', params: { campaignId } });
    },
    deleteCampaign(campaignId) {
      const token = localStorage.getItem('authToken');
      axios
        .delete(`http://127.0.0.1:5000/delete_campaign/${campaignId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(() => {
          this.successMessage = 'Campaign deleted successfully!';
          this.fetchCampaigns();
        })
        .catch(error => {
          console.error("Error deleting campaign:", error);
        });
    },
    logout() {
      localStorage.removeItem('authToken');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', sans-serif;
  background-color: #f4f4f4;
  color: #333;
}

header {
  background-color: #333;
  color: white;
  padding: 20px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-brand {
  font-weight: bold;
  font-size: 24px;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 16px;
}

.nav-link:hover {
  text-decoration: underline;
}

.button.logout {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

/* Page content styling */
.content {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  font-size: 2em;
  font-weight: bold;
}

.create-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.success-message {
  color: red;
  font-weight: bold;
  margin-bottom: 10px;
}

.campaign-card {
  background-color: #fff;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.campaign-card h3 {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.campaign-card p {
  margin: 5px 0;
}

.edit-button, .ad-requests-button, .delete-button {
  background-color: green;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
  font-size: 0.9em;
}

.delete-button {
  background-color: #dc3545;
}
</style>
