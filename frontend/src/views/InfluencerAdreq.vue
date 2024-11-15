<template>
  <div>
    <!-- Navigation Bar -->
    <header>
      <div class="navbar-brand">Influencer @ SPOC</div>
      <div class="user-actions">
        <router-link to="/influencer-dashboard" class="nav-link">Profile</router-link>
        <router-link :to="`/influencer/ad-requests/${influencerId}`" class="nav-link">Ad Management</router-link>
        <router-link to="/find" class="nav-link">Find</router-link>
        <button class="button logout" @click="logout">Logout</button>
      </div>
    </header>
    
    <!-- Ad Management Section -->
    <div class="ad-management">
      <h2>Ad Management for {{ influencerName }}</h2>
      <div v-for="section in sections" :key="section.title">
        <h3>{{ section.title }}</h3>
        <table>
          <thead>
            <tr>
              <th>Campaign Name</th>
              <th>Requirements</th>
              <th>Payment Amount</th>
              <th>Status</th>
              <th v-if="section.title === 'Pending Requests'">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="adRequest in section.requests" :key="adRequest.id">
              <td>{{ adRequest.campaign_name }}</td>
              <td>{{ adRequest.requirements }}</td>
              <td>${{ adRequest.payment_amount.toFixed(2) }}</td>
              <td>{{ adRequest.status }}</td>
              <td v-if="section.title === 'Pending Requests'">
                <button @click="acceptAdRequest(adRequest)">Accept</button>
                <button @click="rejectAdRequest(adRequest)">Reject</button>
                <button @click="negotiateAdRequest(adRequest)">Negotiate</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="section.requests.length === 0">No {{ section.title.toLowerCase() }} found.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['influencerId'],
  data() {
    return {
      influencerName: "inf", // Replace this with the actual influencer's name if available
      adRequests: [],
    };
  },
  computed: {
    sections() {
      return [
        { title: 'New Negotiations', requests: this.adRequests.filter(ad => ad.status === 'Request Negotiated') },
        { title: 'Pending Requests', requests: this.adRequests.filter(ad => ad.status === 'Request Sent') },
        { title: 'Active Requests', requests: this.adRequests.filter(ad => ad.status === 'Request Accepted') },
        { title: 'Rejected Requests', requests: this.adRequests.filter(ad => ad.status === 'Request Rejected') }
      ];
    },
  },
  created() {
    this.fetchAdRequests();
  },
  methods: {
    fetchAdRequests() {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error("Authentication token not found. Please log in.");
        this.$router.push('/'); // Redirect to login if token is missing
        return;
      }
      axios.get(`http://127.0.0.1:5000/influencer/ad_requests/${this.influencerId}`, {
        headers: { 'Authentication-Token': token }
      })
      .then(response => {
        this.adRequests = response.data.ad_requests;
      })
      .catch(error => {
        console.error("Error fetching ad requests:", error);
        if (error.response && error.response.status === 401) {
          alert("Unauthorized access. Please log in again.");
          this.$router.push('/');
        }
      });
    },
    acceptAdRequest(adRequest) {
      const token = localStorage.getItem('authToken');
      axios.put(`http://127.0.0.1:5000/accept_ad_request/${adRequest.id}`, null, {
        headers: { 'Authentication-Token': token }
      })
      .then(() => {
        adRequest.status = "Request Accepted";
        alert("Ad request accepted successfully!");
      })
      .catch(error => {
        console.error("Error accepting ad request:", error);
        alert(error.response.data.error || "Failed to accept ad request.");
      });
    },
    rejectAdRequest(adRequest) {
      const token = localStorage.getItem('authToken');
      axios.put(`http://127.0.0.1:5000/reject_ad_request/${adRequest.id}`, null, {
        headers: { 'Authentication-Token': token }
      })
      .then(() => {
        adRequest.status = "Request Rejected";
        alert("Ad request rejected successfully!");
      })
      .catch(error => {
        console.error("Error rejecting ad request:", error);
        alert(error.response.data.error || "Failed to reject ad request.");
      });
    },
    negotiateAdRequest(adRequest) {
      const token = localStorage.getItem('authToken');
      const updatedData = {
        requirements: adRequest.requirements,
        payment_amount: adRequest.payment_amount,
      };
      axios.put(`http://127.0.0.1:5000/negotiate_ad_request/${adRequest.id}`, updatedData, {
        headers: { 'Authentication-Token': token }
      })
      .then(() => {
        adRequest.status = "Request Negotiated";
        alert("Ad request negotiated successfully!");
      })
      .catch(error => {
        console.error("Error negotiating ad request:", error);
        alert(error.response.data.error || "Failed to negotiate ad request.");
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
/* Navbar Styles */
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

/* Ad Management Styles */
.ad-management {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
}

h3 {
  margin-top: 20px;
  font-weight: bold;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

table th, table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

button {
  margin: 2px;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 0.9em;
}

button:first-of-type {
  background-color: green;
  color: white;
}

button:nth-of-type(2) {
  background-color: red;
  color: white;
}

button:nth-of-type(3) {
  background-color: orange;
  color: white;
}
</style>
