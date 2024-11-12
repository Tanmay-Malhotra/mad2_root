<template>
  <div class="admin-influencers">
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
    <h1>Influencers</h1>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Platform</th>
          <th>Followers</th>
          <th>Flagged</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="influencer in influencers" :key="influencer.id">
          <td>{{ influencer.name }}</td>
          <td>{{ influencer.username }}</td>
          <td>{{ influencer.email }}</td>
          <td>{{ influencer.platform }}</td>
          <td>{{ influencer.followers }}</td>
          <td>{{ influencer.flagged }}</td>
          <td>
            <button @click="toggleFlag(influencer.id)" :class="['flag-btn', influencer.flagged === 'yes' ? 'flagged' : '']">
              {{ influencer.flagged === 'yes' ? 'Unflag' : 'Flag' }}
            </button>
            <button @click="deleteInfluencer(influencer.id)" class="delete-btn">Delete</button>
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
  name: 'AdminInfluencers',
  data() {
    return {
      influencers: [],
      errorMessage: ''
    };
  },
  mounted() {
    this.fetchInfluencers();
  },
  methods: {
    fetchInfluencers() {
      const token = localStorage.getItem('authToken');
      if (!token) {
        this.$router.push('/');
        return;
      }    
      axios
        .get('http://127.0.0.1:5000/admin/influencers', {
          headers: {
            'Authentication-Token': token
          }
        })
        .then(response => {
          this.influencers = response.data.influencers;
        })
        .catch(error => {
          console.error("Error fetching influencers:", error);
          this.errorMessage = 'An error occurred while fetching influencers. Please try again later.';
        });
    },
    toggleFlag(influencerId) {
      const token = localStorage.getItem('authToken');
      axios
        .put(`http://127.0.0.1:5000/influencer/toggle_flag/${influencerId}`, {}, {
          headers: {
            'Authentication-Token': token
          }
        })
        .then(response => {
          const updatedFlaggedStatus = response.data.new_flagged_status;
          this.influencers = this.influencers.map(influencer =>
            influencer.id === influencerId ? { ...influencer, flagged: updatedFlaggedStatus } : influencer
          );
        })
        .catch(error => {
          console.error("Error toggling flag:", error);
          this.errorMessage = 'An error occurred while updating the flag status. Please try again later.';
        });
    },
    deleteInfluencer(influencerId) {
      const token = localStorage.getItem('authToken');
      axios
        .delete(`http://127.0.0.1:5000/admin/influencer/delete/${influencerId}`, {
          headers: {
            'Authentication-Token': token
          }
        })
        .then(() => { // Removed 'response' here to fix the ESLint error
          this.influencers = this.influencers.filter(influencer => influencer.id !== influencerId);
        })
        .catch(error => {
          console.error("Error deleting influencer:", error);
          this.errorMessage = 'An error occurred while deleting the influencer. Please try again later.';
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
.admin-influencers {
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
