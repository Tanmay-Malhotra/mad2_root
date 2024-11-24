<template>
  <div class="edit-ad-request">

    <div class="header">
      <h1>Edit Ad Request</h1>
      <button @click="goBack" class="button go-back-button">Go Back</button>
    </div>
    
    <form @submit.prevent="updateAdRequest">

      <div class="form-group">
        <label for="requirements">Requirements:</label>
        <textarea v-model="requirements" rows="4"></textarea>
      </div>

    
      <div class="form-group">
        <label for="payment_amount">Payment Amount:</label>
        <input type="number" v-model="payment_amount" />
      </div>

      <button type="submit" class="button update-request-button">Update Ad Request</button>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditAdRequest',
  props: ['adRequestId', 'campaignId'],
  data() {
    return {
      requirements: '',
      payment_amount: '',
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {

    updateAdRequest() {
      const token = localStorage.getItem('authToken');
      const updatedFields = {
        requirements: this.requirements,
        payment_amount: this.payment_amount
      };

      axios
        .put(
          `http://127.0.0.1:5000/campaign/update_ad_request/${this.adRequestId}`,
          updatedFields,
          { headers: { 'Authentication-Token': token } }
        )
        .then(() => {
          this.successMessage = "Ad request updated successfully!";
          this.errorMessage = '';
        })
        .catch(error => {
          console.error("Error updating ad request:", error);
          this.errorMessage = error.response.data.error || "Failed to update ad request.";
          this.successMessage = '';
        });
    },

    goBack() {
      this.$router.push({ name: 'ViewAdRequests', params: { campaignId: this.campaignId } });
    }
  }
};
</script>

<style scoped>
.edit-ad-request {
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

.go-back-button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
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

.button.update-request-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
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
