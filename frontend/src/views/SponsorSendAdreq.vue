<template>
  <div class="send-ad-request">
    <h1>Send Ad Request to {{ influencerName }}</h1>
    <form @submit.prevent="submitAdRequest">
      <!-- Select Campaign Dropdown -->
      <div class="form-group">
        <label for="campaign">Select Campaign:</label>
        <select v-model="campaign_id" required>
          <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">{{ campaign.name }}</option>
        </select>
      </div>

      <!-- Requirements Textarea -->
      <div class="form-group">
        <label for="requirements">Requirements:</label>
        <textarea v-model="requirements" rows="4" required></textarea>
      </div>

      <!-- Payment Amount Input -->
      <div class="form-group">
        <label for="payment_amount">Payment Amount:</label>
        <input type="number" v-model="payment_amount" required />
      </div>

      <!-- Submit Button -->
      <button type="submit" class="button send-request-button">Send Ad Request</button>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SendAdRequest',
  props: ['influencerId', 'influencerName'],
  data() {
    return {
      campaigns: [],
      campaign_id: '',
      requirements: '',
      payment_amount: '',
      errorMessage: ''
    };
  },
  created() {
    this.fetchCampaigns();
  },
  methods: {
    // Fetch available campaigns for the sponsor
    fetchCampaigns() {
      const token = localStorage.getItem('authToken');
      const sponsorId = localStorage.getItem('sponsorId');
      axios
        .get(`http://127.0.0.1:5000/campaigns/${sponsorId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.campaigns = response.data.campaigns;
        })
        .catch(error => {
          console.error("Error fetching campaigns:", error);
          this.errorMessage = "Error fetching campaigns.";
        });
    },
    // Submit the ad request to the selected influencer
    submitAdRequest() {
      const token = localStorage.getItem('authToken');
      axios
        .post(`http://127.0.0.1:5000/sponsor/campaign/ad_request/${this.influencerId}`, {
          campaign_id: this.campaign_id,
          requirements: this.requirements,
          payment_amount: this.payment_amount
        }, {
          headers: { 'Authentication-Token': token }
        })
        // eslint-disable-next-line
        .then(response => {
          alert("Ad request sent successfully!"); // Display success message
          this.$router.push('/find-influencers'); // Redirect to Find Influencers page
        })
        .catch(error => {
          console.error("Error sending ad request:", error);
          this.errorMessage = error.response.data.error || "Failed to send ad request.";
        });
    }
  }
};
</script>

<style scoped>
.send-ad-request {
  width: 50%;
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

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

select, textarea, input[type="number"] {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

textarea {
  resize: none;
}

.button.send-request-button {
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  border-radius: 5px;
  cursor: pointer;
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
