<template>
  <div>
    <header>
      <div class="navbar-brand">Sponsor @ SPOC</div>
      <div class="user-actions">
        <router-link to="/sponsor-dashboard" class="nav-link">Profile</router-link>
        <router-link to="/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="/find-influencers" class="nav-link">Find</router-link>
        <button class="button logout" @click="logout">Logout</button>
      </div>
    </header>
    
    <div class="find-influencers content">
      <h1>Find Influencers</h1>
      <div class="search-bar">
        <label for="search">Search:</label>
        <input type="text" v-model="searchQuery" placeholder="Enter name or platform" @input="fetchInfluencers" />
      </div>
      <table class="influencer-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Industry</th>
            <th>Platform</th>
            <th>Followers</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="influencer in influencers" :key="influencer.id">
            <td>{{ influencer.name }}</td>
            <td>{{ influencer.industry }}</td>
            <td>{{ influencer.platform }}</td>
            <td>{{ influencer.followers }}</td>
            <td>
              <button @click="sendAdRequest(influencer.id, influencer.name)" class="send-request">
                Send Ad Request
              </button>
            </td>
          </tr>
          <tr v-if="influencers.length === 0">
            <td colspan="5">No influencers found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SponsorFindInf',
  data() {
    return {
      influencers: [],
      searchQuery: ''
    };
  },
  created() {
    this.fetchInfluencers();
  },
  methods: {
    fetchInfluencers() {
      const token = localStorage.getItem('authToken');
      const params = {
        search: this.searchQuery
      };
      axios
        .get('http://127.0.0.1:5000/sponsor/inf_find', {
          headers: { 'Authentication-Token': token },
          params
        })
        .then(response => {
          this.influencers = response.data.influencers;
        })
        .catch(error => {
          console.error("Error fetching influencers:", error);
        });
    },
    sendAdRequest(influencerId, influencerName) {
      
      this.$router.push({
        name: 'SponsorSendAdreq',
        params: { influencerId },
        query: { name: influencerName }
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

.content {
  padding: 20px;
}

.find-influencers {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 1.8em;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar label {
  margin-right: 10px;
  font-weight: bold;
}

.search-bar input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.influencer-table {
  width: 100%;
  border-collapse: collapse;
}

.influencer-table th, .influencer-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.influencer-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.send-request {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
}

.send-request:hover {
  background-color: #0056b3;
}
</style>
