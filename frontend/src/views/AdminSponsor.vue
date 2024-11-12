<template>
  <div class="admin-sponsor">
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
    <h1>Sponsors</h1>

    <!-- Approved Sponsors Table -->
    <div class="table-container">
      <h2>Approved Sponsors</h2>
      <table class="sponsor-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Industry</th>
            <th>Flagged</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sponsor in approvedSponsors" :key="sponsor.id">
            <td>{{ sponsor.name }}</td>
            <td>{{ sponsor.user.email }}</td>
            <td>{{ sponsor.industry }}</td>
            <td>{{ sponsor.flagged }}</td>
            <td>
              <button class="button flag" @click="toggleFlag(sponsor.id)">Flag</button>
              <button class="button delete" @click="deleteSponsor(sponsor.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- New Sponsor Requests Table -->
    <div class="table-container">
      <h2>New Sponsor Requests</h2>
      <table class="sponsor-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Industry</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sponsor in newSponsorRequests" :key="sponsor.id">
            <td>{{ sponsor.name }}</td>
            <td>{{ sponsor.user.email }}</td>
            <td>{{ sponsor.industry }}</td>
            <td>
              <button class="button approve" @click="approveSponsor(sponsor.id)">Approve</button>
              <button class="button reject" @click="rejectSponsor(sponsor.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SponsorsDashboard',
  data() {
    return {
      approvedSponsors: [],
      newSponsorRequests: []
    };
  },
  mounted() {
    this.fetchSponsors();
  },
  methods: {
    
    fetchSponsors() {
      const token = localStorage.getItem('authToken');
        if (!token) {
        this.$router.push('/');
        return;
        }
      axios
        .get('http://127.0.0.1:5000/admin/sponsors', {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          // Separating approved sponsors and pending requests based on 'approved' field
          this.approvedSponsors = response.data.sponsors.filter(sponsor => sponsor.approved === true);
          this.newSponsorRequests = response.data.sponsors.filter(sponsor => sponsor.approved === false);
        })
        .catch(error => {
          console.error("Error fetching sponsors:", error);
        });
    },
    approveSponsor(sponsorId) {
      axios
        .put(`http://127.0.0.1:5000/sponsor/approve/${sponsorId}`, null, {
          headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        })
        .then(() => {
          this.fetchSponsors();
        })
        .catch(error => {
          console.error("Error approving sponsor:", error);
        });
    },
    rejectSponsor(sponsorId) {
      axios
        .put(`http://127.0.0.1:5000/sponsor/reject/${sponsorId}`, null, {
          headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        })
        .then(() => {
          this.fetchSponsors();
        })
        .catch(error => {
          console.error("Error rejecting sponsor:", error);
        });
    },
    toggleFlag(sponsorId) {
      axios
        .put(`http://127.0.0.1:5000/sponsor/toggle_flag/${sponsorId}`, null, {
          headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        })
        .then(() => {
          this.fetchSponsors();
        })
        .catch(error => {
          console.error("Error toggling flag status:", error);
        });
    },
    deleteSponsor(sponsorId) {
      axios
        .delete(`http://127.0.0.1:5000/admin/sponsor/delete/${sponsorId}`, {
          headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        })
        .then(() => {
          this.fetchSponsors();
        })
        .catch(error => {
          console.error("Error deleting sponsor:", error);
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

.sponsors-dashboard {
  font-family: 'Roboto', sans-serif;
}

.table-container {
  margin-bottom: 20px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.sponsor-table {
  width: 100%;
  border-collapse: collapse;
}

.sponsor-table th,
.sponsor-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.sponsor-table th {
  font-weight: bold;
}

.button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  color: white;
}

.button.approve {
  background-color: #28a745;
}

.button.reject {
  background-color: #dc3545;
}

.button.flag {
  background-color: #ffc107;
  color: black;
}

.button.delete {
  background-color: #e74c3c;
}

.button:hover {
  opacity: 0.8;
}
</style>
