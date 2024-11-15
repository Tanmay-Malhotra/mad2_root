<template>
  <div class="ad-requests" v-if="campaignId">
    <!-- Header with Go Back Button and Title -->
    <div class="header">
      <h1>Ad Requests for Campaign: {{ campaignName }}</h1>
      <button @click="goBack" class="button go-back-button">Go Back</button>
    </div>

    <!-- Display ad request sections if there are any requests, else show the no ad requests message -->
    <div v-if="adRequests.length > 0">
      <!-- Ad request sections for different statuses -->
      <div class="request-section" v-for="section in sections" :key="section.status">
        <h2>{{ section.title }}</h2>
        <table v-if="section.requests.length">
          <thead>
            <tr>
              <th>Influencer Name</th>
              <th>Requirements</th>
              <th>Payment Amount</th>
              <th>Status</th>
              <th v-if="sectionHasActions(section.status)">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="adRequest in section.requests" :key="adRequest.id">
              <td>{{ adRequest.influencer_name }}</td>
              <td>{{ adRequest.requirements }}</td>
              <td>${{ adRequest.payment_amount }}</td>
              <td>{{ adRequest.status }}</td>
              <!-- Actions for Pending Requests -->
              <td v-if="section.status === 'Request Sent'">
                <button @click="redirectToEdit(adRequest.id)" class="button edit-button">Edit</button>
                <button @click="deleteAdRequest(adRequest.id)" class="button delete-button">Delete</button>
              </td>
              <!-- Actions for Negotiated Requests -->
              <td v-else-if="section.status === 'Request Negotiated'">
                <button @click="acceptAdRequest(adRequest.id)" class="button accept-button">Accept</button>
                <button @click="rejectAdRequest(adRequest.id)" class="button reject-button">Reject</button>
              </td>
              <!-- Actions for Requests Sent by Influencer -->
              <td v-else-if="section.status === 'Request Sent by Influencer'">
                <button @click="acceptInfluencerAdRequest(adRequest.id)" class="button accept-button">Accept</button>
                <button @click="rejectInfluencerAdRequest(adRequest.id)" class="button reject-button">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>No {{ section.title.toLowerCase() }} found.</p>
      </div>
    </div>

    <!-- No ad requests message -->
    <p v-if="adRequests.length === 0">No ad requests available for this campaign.</p>

    <!-- Error and Success Messages -->
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
    // Categorize ad requests based on status
    sections() {
      return [
        { title: 'Requests Sent by Influencer', status: 'Request Sent by Influencer', requests: this.adRequests.filter(req => req.status === 'Request Sent by Influencer') },
        { title: 'New Negotiations', status: 'Request Negotiated', requests: this.adRequests.filter(req => req.status === 'Request Negotiated') },
        { title: 'Pending Requests', status: 'Request Sent', requests: this.adRequests.filter(req => req.status === 'Request Sent') },
        { title: 'Active Requests', status: 'Request Accepted', requests: this.adRequests.filter(req => req.status === 'Request Accepted') },
        { title: 'Rejected Requests', status: 'Request Rejected', requests: this.adRequests.filter(req => req.status === 'Request Rejected') }
      ];
    }
  },
  created() {
    // Redirect if campaignId is missing
    if (!this.campaignId) {
      this.goBack();
    } else {
      this.fetchAdRequests();
    }
  },
  methods: {
    fetchAdRequests() {
      const token = localStorage.getItem('authToken');
      axios
        .get(`http://127.0.0.1:5000/sponsor/campaign/${this.campaignId}/ad_requests`, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.adRequests = response.data.ad_requests || [];
          if (this.adRequests.length === 0) {
            this.successMessage = "No ad requests available for this campaign.";
          }
        })
        .catch(error => {
          console.error("Error fetching ad requests:", error);
          this.errorMessage = "Error fetching ad requests.";
        });
    },
    goBack() {
      this.$router.push('/campaigns');
    },
    redirectToEdit(adRequestId) {
      this.$router.push({ name: 'SponsorUpdateadreq', params: { adRequestId, campaignId: this.campaignId } });
    },
    deleteAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      axios
        .delete(`http://127.0.0.1:5000/campaign/delete_ad_request/${adRequestId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(() => {
          // Filter out the deleted request
          this.adRequests = this.adRequests.filter(adRequest => adRequest.id !== adRequestId);
          this.successMessage = "Ad request deleted successfully!";
          this.errorMessage = '';

          // If no ad requests left, show the no ad requests message
          if (this.adRequests.length === 0) {
            this.successMessage = "No ad requests available for this campaign.";
          }
        })
        .catch(error => {
          console.error("Error deleting ad request:", error);
          this.errorMessage = error.response?.data?.error || "Failed to delete ad request.";
          this.successMessage = '';
        });
    },
    // Accept negotiated ad request
    acceptAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      const url = `http://127.0.0.1:5000/accept_negotiated_ad_request/${adRequestId}`;
      axios
        .put(url, null, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.successMessage = response.data.message || "Ad request accepted successfully!";
          this.errorMessage = '';
          this.fetchAdRequests(); // Refresh the requests to update status
        })
        .catch(error => {
          console.error("Error accepting ad request:", error);
          this.errorMessage = error.response?.data?.error || "Failed to accept ad request.";
          this.successMessage = '';
        });
    },
    // Reject negotiated ad request
    rejectAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      const url = `http://127.0.0.1:5000/reject_negotiated_ad_request/${adRequestId}`;
      axios
        .put(url, null, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.successMessage = response.data.message || "Ad request rejected successfully!";
          this.errorMessage = '';
          this.fetchAdRequests(); // Refresh the requests to update status
        })
        .catch(error => {
          console.error("Error rejecting ad request:", error);
          this.errorMessage = error.response?.data?.error || "Failed to reject ad request.";
          this.successMessage = '';
        });
    },
    // Accept ad request sent by influencer
    acceptInfluencerAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      const url = `http://127.0.0.1:5000/accept_influencer_ad_request/${adRequestId}`;
      axios
        .put(url, null, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.successMessage = response.data.message || "Ad request accepted successfully!";
          this.errorMessage = '';
          this.fetchAdRequests(); // Refresh the requests to update status
        })
        .catch(error => {
          console.error("Error accepting influencer ad request:", error);
          this.errorMessage = error.response?.data?.error || "Failed to accept ad request.";
          this.successMessage = '';
        });
    },
    // Reject ad request sent by influencer
    rejectInfluencerAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      const url = `http://127.0.0.1:5000/reject_influencer_ad_request/${adRequestId}`;
      axios
        .put(url, null, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.successMessage = response.data.message || "Ad request rejected successfully!";
          this.errorMessage = '';
          this.fetchAdRequests(); // Refresh the requests to update status
        })
        .catch(error => {
          console.error("Error rejecting influencer ad request:", error);
          this.errorMessage = error.response?.data?.error || "Failed to reject ad request.";
          this.successMessage = '';
        });
    },
    // Determine if the section should display action buttons
    sectionHasActions(status) {
      return status === 'Request Sent' || status === 'Request Negotiated' || status === 'Request Sent by Influencer';
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
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

table th,
table td {
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

.accept-button {
  background-color: #28a745;
  color: white;
  border: none;
}

.reject-button {
  background-color: #dc3545;
  color: white;
  border: none;
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}

.success-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}

</style>