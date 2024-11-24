<template>
  <div>
    <header>
      <div class="navbar-brand">Influencer @ SPOC</div>
      <div class="user-actions">
        <router-link to="/influencer-dashboard" class="nav-link">Profile</router-link>
        <router-link :to="`/influencer/ad-requests/${influencerId}`" class="nav-link">Ad Management</router-link>
        <router-link :to="`/public-campaigns/${influencerId}`" class="nav-link">Find Campaigns</router-link>
        <button class="button logout" @click="logout">Logout</button>
      </div>
    </header>

    <div class="campaigns-list">
      <h1>Find Campaigns</h1>
      <div class="search-bar">
        <label for="search">Search:</label>
        <input type="text" id="search" v-model="searchQuery" placeholder="Enter campaign name or category" />
      </div>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Category</th>
            <th>Budget</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Sponsor</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="campaign in filteredCampaigns" :key="campaign.id">
            <td>{{ campaign.name }}</td>
            <td>{{ campaign.category }}</td>
            <td>${{ campaign.budget }}</td>
            <td>{{ campaign.start_date }}</td>
            <td>{{ campaign.end_date || 'Not specified' }}</td>
            <td>{{ campaign.sponsor_name }}</td>
            <td>
              <button class="send-request-button" @click="sendAdRequest(campaign.id)">Send Ad Request</button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-if="filteredCampaigns.length === 0">No campaigns found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PublicCampaigns',
  data() {
    return {
      searchQuery: '',
      campaigns: [],
      influencerId: localStorage.getItem('influencerId') 
    };
  },
  computed: {
    filteredCampaigns() {
      return this.campaigns.filter(
        campaign =>
          campaign.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          campaign.category.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  mounted() {
    this.fetchPublicCampaigns();
  },
  methods: {
    fetchPublicCampaigns() {
      const token = localStorage.getItem('authToken');
      axios
        .get(`http://127.0.0.1:5000/influencer/public_campaigns/${this.influencerId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.campaigns = response.data.public_campaigns;
        })
        .catch(error => {
          console.error("Error fetching public campaigns:", error);
        });
    },
    sendAdRequest(campaignId, campaignName) {
    
    this.$router.push({
      name: 'InfluencerSendAdRequest',
      params: { campaignId: campaignId },
      query: { name: campaignName, influencerId: this.influencerId }
    })},
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

.campaigns-list {
  max-width: 800px;
  margin: 20px auto;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.campaigns-list h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
}

.search-bar input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th,
table td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}

.send-request-button {
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.send-request-button:hover {
  background-color: #0056b3;
}

p {
  font-size: 16px;
  margin-top: 20px;
}
</style>
