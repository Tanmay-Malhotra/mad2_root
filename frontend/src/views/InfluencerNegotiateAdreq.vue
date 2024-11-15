<template>
  <div class="negotiate-ad-request">
    <h1>Negotiate Ad Request for Campaign: {{ campaignName }}</h1>
    <form @submit.prevent="submitNegotiation">
      <!-- Requirements Textarea -->
      <div class="form-group">
        <label for="requirements">Requirements:</label>
        <textarea v-model="requirements" rows="3"></textarea>
      </div>

      <!-- Payment Amount Input -->
      <div class="form-group">
        <label for="payment_amount">Payment Amount:</label>
        <input type="number" v-model="paymentAmount" />
      </div>

      <!-- Submit Button -->
      <button type="submit" class="button submit-button">Send Negotiated Request</button>

      <!-- Success and Error Messages -->
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfluencerNegotiateAdRequest',
  props: ['adRequestId', 'campaignName'],
  data() {
    return {
      requirements: '',
      paymentAmount: '',
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    // Submit the negotiation request
    submitNegotiation() {
      const token = localStorage.getItem('authToken');
      const updatedData = {
        requirements: this.requirements,
        payment_amount: this.paymentAmount
      };

      axios
        .put(`http://127.0.0.1:5000/negotiate_ad_request/${this.adRequestId}`, updatedData, {
          headers: { 'Authentication-Token': token }
        })
        .then(() => {
          this.successMessage = "Ad request has been negotiated and sent back to sponsor for review.";
          this.errorMessage = '';
        })
        .catch(error => {
          console.error("Error negotiating ad request:", error);
          this.errorMessage = error.response?.data?.error || "Failed to negotiate ad request.";
          this.successMessage = '';
        });
    }
  }
};
</script>

<style scoped>
.negotiate-ad-request {
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

textarea,
input[type="number"] {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.button.submit-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

.success-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}
</style>
