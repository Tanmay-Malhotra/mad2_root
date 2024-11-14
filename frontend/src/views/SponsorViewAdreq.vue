<template>
  <div class="ad-requests">
    <!-- Header with Go Back Button and Title -->
    <div class="header">
      <h1>Ad Requests for Campaign: {{ campaignName }}</h1>
      <button @click="goBack" class="button go-back-button">Go Back</button>
    </div>

    <!-- New Negotiations Section -->
    <div class="request-section">
      <h2>New Negotiations</h2>
      <table v-if="newNegotiations.length">
        <thead>
          <tr>
            <th>Influencer Name</th>
            <th>Requirements</th>
            <th>Payment Amount</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="adRequest in newNegotiations" :key="adRequest.id">
            <td>{{ adRequest.influencer_name }}</td>
            <td>{{ adRequest.requirements }}</td>
            <td>${{ adRequest.payment_amount }}</td>
            <td>{{ adRequest.status }}</td>
            <td>
              <button @click="redirectToEdit(adRequest.id)" class="button edit-button">Edit</button>
              <button @click="deleteAdRequest(adRequest.id)" class="button delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No new negotiations found.</p>
    </div>

    <!-- Pending Requests Section -->
    <div class="request-section">
      <h2>Pending Requests</h2>
      <table v-if="pendingRequests.length">
        <thead>
          <tr>
            <th>Influencer Name</th>
            <th>Requirements</th>
            <th>Payment Amount</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="adRequest in pendingRequests" :key="adRequest.id">
            <td>{{ adRequest.influencer_name }}</td>
            <td>{{ adRequest.requirements }}</td>
            <td>${{ adRequest.payment_amount }}</td>
            <td>{{ adRequest.status }}</td>
            <td>
              <button @click="redirectToEdit(adRequest.id)" class="button edit-button">Edit</button>
              <button @click="deleteAdRequest(adRequest.id)" class="button delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No pending requests found.</p>
    </div>

    <!-- Active Requests Section -->
    <div class="request-section">
      <h2>Active Requests</h2>
      <table v-if="activeRequests.length">
        <thead>
          <tr>
            <th>Influencer Name</th>
            <th>Requirements</th>
            <th>Payment Amount</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="adRequest in activeRequests" :key="adRequest.id">
            <td>{{ adRequest.influencer_name }}</td>
            <td>{{ adRequest.requirements }}</td>
            <td>${{ adRequest.payment_amount }}</td>
            <td>{{ adRequest.status }}</td>
            <td>
              <button @click="redirectToEdit(adRequest.id)" class="button edit-button">Edit</button>
              <button @click="deleteAdRequest(adRequest.id)" class="button delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No active requests found.</p>
    </div>

    <!-- Rejected Requests Section -->
    <div class="request-section">
      <h2>Rejected Requests</h2>
      <table v-if="rejectedRequests.length">
        <thead>
          <tr>
            <th>Influencer Name</th>
            <th>Requirements</th>
            <th>Payment Amount</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="adRequest in rejectedRequests" :key="adRequest.id">
            <td>{{ adRequest.influencer_name }}</td>
            <td>{{ adRequest.requirements }}</td>
            <td>${{ adRequest.payment_amount }}</td>
            <td>{{ adRequest.status }}</td>
            <td>
              <button @click="redirectToEdit(adRequest.id)" class="button edit-button">Edit</button>
              <button @click="deleteAdRequest(adRequest.id)" class="button delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No rejected requests found.</p>
    </div>
    
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CampaignAdRequests',
  props: ['campaignId', 'campaignName'],
  data() {
    return {
      adRequests: [],
      errorMessage: '',
      successMessage: ''
    };
  },
  computed: {
    newNegotiations() {
      return this.adRequests.filter(req => req.status === "Request Negotiated");
    },
    pendingRequests() {
      return this.adRequests.filter(req => req.status === "Request Sent");
    },
    activeRequests() {
      return this.adRequests.filter(req => req.status === "Request Accepted");
    },
    rejectedRequests() {
      return this.adRequests.filter(req => req.status === "Request Rejected");
    }
  },
  created() {
    this.fetchAdRequests();
  },
  methods: {
    // Fetch ad requests for the campaign
    fetchAdRequests() {
      const token = localStorage.getItem('authToken');
      axios
        .get(`http://127.0.0.1:5000/sponsor/campaign/${this.campaignId}/ad_requests`, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.adRequests = response.data.ad_requests;
        })
        .catch(error => {
          console.error("Error fetching ad requests:", error);
          this.errorMessage = "Error fetching ad requests.";
        });
    },
    // Go back to the campaigns page
    goBack() {
      this.$router.push('/campaigns');
    },
    // Redirect to the Edit Ad Request page
    redirectToEdit(adRequestId) {
      this.$router.push({ name: 'EditAdRequest', params: { adRequestId } });
    },
    // Delete the ad request
    deleteAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      axios
        .delete(`http://127.0.0.1:5000/campaign/delete_ad_request/${adRequestId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(() => {
          this.adRequests = this.adRequests.filter(adRequest => adRequest.id !== adRequestId);
          this.successMessage = "Ad request deleted successfully!";
          this.errorMessage = '';
        })
        .catch(error => {
          console.error("Error deleting ad request:", error);
          this.errorMessage = error.response.data.error || "Failed to delete ad request.";
          this.successMessage = '';
        });
    }
  }
};
</script>

<style scoped>
.ad-requests {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  font-size: 1.8em;
  font-weight: bold;
}

.go-back-button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.request-section {
  margin-top: 20px;
}

.request-section h2 {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

table th, table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.button {
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
}

.edit-button {
  background-color: green;
  color: white;
  border: none;
}

.delete-button {
  background-color: red;
  color: white;
  border: none;
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

.success-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}
</style>
