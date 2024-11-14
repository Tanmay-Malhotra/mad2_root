<template>
  <div class="ad-requests">
    <!-- Header with Go Back Button and Title -->
    <div class="header">
      <h1>Ad Requests for Campaign</h1>
      <button @click="goBack" class="button go-back-button">Go Back</button>
    </div>
    
    <!-- Ad Requests Table -->
    <table class="ad-requests-table">
      <thead>
        <tr>
          <th>Requirements</th>
          <th>Payment Amount</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="adRequest in adRequests" :key="adRequest.id">
          <td>{{ adRequest.requirements }}</td>
          <td>{{ adRequest.payment_amount }}</td>
          <td>{{ adRequest.status }}</td>
          <td>
            <button @click="redirectToEdit(adRequest.id)" class="button edit-button">Edit</button>
            <button @click="deleteAdRequest(adRequest.id)" class="button delete-button">Delete</button>
          </td>
        </tr>
        <tr v-if="adRequests.length === 0">
          <td colspan="4">No ad requests found for this campaign.</td>
        </tr>
      </tbody>
    </table>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CampaignAdRequests',
  props: ['campaignId'],
  data() {
    return {
      adRequests: [],
      errorMessage: '',
      successMessage: ''
    };
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
        // eslint-disable-next-line
        .then(response => {
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

.ad-requests-table {
  width: 100%;
  border-collapse: collapse;
}

.ad-requests-table th, .ad-requests-table td {
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
