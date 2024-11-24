<template>
  <div class="send-ad-request">
   
    <div class="header">
      <h1>Send Ad Request to Sponsor for {{ campaignName }}</h1>
      <button @click="goBack" class="button go-back-button">Go Back</button>
    </div>

    <form @submit.prevent="submitAdRequest">
      
      <div class="form-group">
        <label for="requirements">Requirements:</label>
        <textarea v-model="requirements" rows="4" required></textarea>
      </div>

     
      <div class="form-group">
        <label for="payment_amount">Payment Amount:</label>
        <input type="number" v-model="payment_amount" required />
      </div>


      <button type="submit" class="button send-request-button">Send Ad Request</button>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfluencerSendAdRequest',
  props: ['campaignId', 'campaignName', 'influencerId'],
  data() {
    return {
      requirements: '',
      payment_amount: '',
      errorMessage: ''
    };
  },
  methods: {
    
    submitAdRequest() {
    const token = localStorage.getItem('authToken');
    axios
      .post(`http://127.0.0.1:5000/influencer/campaign/ad_request/${this.campaignId}`, {
        requirements: this.requirements,
        payment_amount: this.payment_amount
      }, {
        headers: { 'Authentication-Token': token }
      })
      // eslint-disable-next-line
      .then(response => {
        alert("Ad request sent to sponsor successfully!");
        
        this.$router.push({ name: 'InfluencerFindCampaigns', params: { influencerId: this.influencerId } });
      })
      .catch(error => {
        console.error("Error sending ad request:", error);
        this.errorMessage = error.response.data.error || "Failed to send ad request.";
      });
    },
  
    goBack() {
        this.$router.push({ name: 'InfluencerFindCampaigns', params: { influencerId: this.influencerId } });
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

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

textarea, input[type="number"] {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

textarea {
  resize: none;
}

.button {
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.send-request-button {
  background-color: #28a745;
  color: #fff;
  border: none;
}

.go-back-button {
  background-color: #6c757d;
  color: white;
  border: none;
  font-size: 1em;
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
