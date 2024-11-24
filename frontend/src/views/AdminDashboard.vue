<template>
  <div class="admin-dashboard">
    
    <header class="navbar">
      <div class="navbar-brand">SPOC Administrator</div>
      <div class="navbar-links">
        <router-link to="/admin-dashboard" class="nav-link">Home</router-link>
        <router-link to="/admin/sponsors" class="nav-link">Sponsors</router-link>
        <router-link to="admin/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="admin/influencers" class="nav-link">Influencers</router-link>
        <button class="nav-link logout" @click="logout">Logout</button>
      </div>
    </header>

    
    <h1>Welcome, Admin</h1>
    <h2>Manage SPOC</h2>
    <div class="stats-cards">
      <div class="card" v-for="stat in stats" :key="stat.label">
        <h3>{{ stat.label }}</h3>
        <p>{{ stat.value }}</p>
      </div>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: [
        { label: 'Total Users', value: 0 },
        { label: 'Number of Sponsors', value: 0 },
        { label: 'Number of Influencers', value: 0 },
        { label: 'Number of Campaigns', value: 0 },
        { label: 'Active Ad Requests', value: 0 },
        { label: 'Flagged Sponsors', value: 0 },
        { label: 'Flagged Influencers', value: 0 },
        { label: 'Flagged Campaigns', value: 0 },
        { label: 'Flagged Ad Requests', value: 0 }
      ],
      errorMessage: ''
    };
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    fetchStats() {
      const token = localStorage.getItem('authToken');

      if (!token) {
        this.$router.push('/');
        return;
      }

      axios
        .get('http://127.0.0.1:5000/admin_dashboard', {
          headers: {
            'Authentication-Token': token
          }
        })
        .then(response => {
          const data = response.data;
          this.stats[0].value = data.total_users;
          this.stats[1].value = data.number_of_sponsors;
          this.stats[2].value = data.number_of_influencers;
          this.stats[3].value = data.number_of_campaigns;
          this.stats[4].value = data.active_ad_requests;
          this.stats[5].value = data.flagged_sponsors;
          this.stats[6].value = data.flagged_influencers;
          this.stats[7].value = data.flagged_campaigns;
          this.stats[8].value = data.flagged_ad_requests;
        })
        .catch(error => {
          console.error("Error fetching stats:", error);
          if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            localStorage.removeItem('authToken');
            this.$router.push('/');
          } else {
            this.errorMessage = 'An error occurred while fetching statistics. Please try again later.';
          }
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

body {
  font-family: 'Roboto', sans-serif;
  background-color: #f4f4f4;
  color: #333;
  margin: 0;
}


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


.stats-cards {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.card {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  width: 200px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.card p {
  font-size: 24px;
  color: #007bff;
  margin: 10px 0 0;
}

.error-message {
  color: #e74c3c;
  margin-top: 20px;
}
</style>
