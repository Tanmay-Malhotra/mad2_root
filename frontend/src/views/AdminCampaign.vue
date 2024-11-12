<template>
  <div class="admin-campaigns">
    <header class="navbar">
      <div class="navbar-brand">SPOC Administrator</div>
      <div class="navbar-links">
        <router-link to="/admin-dashboard" class="nav-link">Home</router-link>
        <router-link to="/admin/sponsors" class="nav-link">Sponsors</router-link>
        <router-link to="/admin/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="/admin/influencers" class="nav-link">Influencers</router-link>
        <button class="nav-link logout" @click="logout">Logout</button>
      </div>
    </header>
    <h1>Campaigns</h1>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Status</th>
          <th>Category</th>
          <th>Budget</th>
          <th>Flagged</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="campaign in campaigns" :key="campaign.id">
          <td>{{ campaign.name }}</td>
          <td>{{ campaign.status }}</td>
          <td>{{ campaign.category }}</td>
          <td>{{ campaign.budget }}</td>
          <td>{{ campaign.flagged }}</td>
          <td>
            <button @click="toggleFlag(campaign.id)" :class="['flag-btn', campaign.flagged === 'yes' ? 'flagged' : '']">
              {{ campaign.flagged === 'yes' ? 'Unflag' : 'Flag' }}
            </button>
            <button @click="deleteCampaign(campaign.id)" class="delete-btn">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminCampaigns',
  data() {
    return {
      campaigns: [],
      errorMessage: ''
    };
  },
  mounted() {
    this.fetchCampaigns();
  },
  methods: {
    fetchCampaigns() {
      const token = localStorage.getItem('authToken');
      if (!token) {
        this.$router.push('/');
        return;
      }
      axios
        .get('http://127.0.0.1:5000/admin/campaigns', {
          headers: {
            'Authentication-Token': token
          }
        })
        .then(response => {
          this.campaigns = response.data.campaigns;
        })
        .catch(error => {
          console.error("Error fetching campaigns:", error);
          this.errorMessage = 'An error occurred while fetching campaigns. Please try again later.';
        });
    },
    toggleFlag(campaignId) {
      const token = localStorage.getItem('authToken');
      axios
        .put(`http://127.0.0.1:5000/campaign/toggle_flag/${campaignId}`, {}, {
          headers: {
            'Authentication-Token': token
          }
        })
        .then(response => {
          const updatedCampaign = response.data.new_flagged_status;
          this.campaigns = this.campaigns.map(campaign =>
            campaign.id === campaignId ? { ...campaign, flagged: updatedCampaign } : campaign
          );
        })
        .catch(error => {
          console.error("Error toggling flag:", error);
          this.errorMessage = 'An error occurred while updating the flag status. Please try again later.';
        });
    },
    deleteCampaign(campaignId) {
      const token = localStorage.getItem('authToken');
      axios
        .delete(`http://127.0.0.1:5000/admin/campaign/delete/${campaignId}`, {
          headers: {
            'Authentication-Token': token
          }
        })
        .then(() => {
          this.campaigns = this.campaigns.filter(campaign => campaign.id !== campaignId);
        })
        .catch(error => {
          console.error("Error deleting campaign:", error);
          this.errorMessage = 'An error occurred while deleting the campaign. Please try again later.';
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
/* Navbar styling */
.navbar {
  background-color: #333;
  color: white;
  padding: 20px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-weight: bold;
  font-size: 20px;
}

.navbar-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 16px;
  cursor: pointer;
}

.nav-link:hover {
  text-decoration: underline;
}

.logout {
  background-color: transparent;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
.admin-campaigns {
  
  background-color: #f4f4f4;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  font-weight: bold;
}

.flag-btn {
  background-color: #ffcc00;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  color: #333;
  border-radius: 4px;
  font-size: 14px;
}

.flagged {
  background-color: #f44336;
  color: white;
}

.delete-btn {
  background-color: #e74c3c;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  color: white;
  border-radius: 4px;
  font-size: 14px;
  margin-left: 8px;
}

.error-message {
  color: #e74c3c;
  margin-top: 20px;
}
</style>
