<template>
  <div>
    <h1>Ad Requests for {{ campaignName }}</h1>
    <div v-for="adRequest in adRequests" :key="adRequest.id" class="ad-request-card">
      <p>Requirements: {{ adRequest.requirements }}</p>
      <p>Payment Amount: {{ adRequest.payment_amount }}</p>
      <p>Status: {{ adRequest.status }}</p>
      <button @click="deleteAdRequest(adRequest.id)" class="button delete-button">Delete</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ViewAdRequests',
  props: ['campaignId'],
  data() {
    return {
      adRequests: [],
      campaignName: ''
    };
  },
  mounted() {
    this.fetchAdRequests();
  },
  methods: {
    fetchAdRequests() {
      const token = localStorage.getItem('authToken');
      axios
        .get(`http://127.0.0.1:5000/view_ad_requests/${this.campaignId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(response => {
          this.adRequests = response.data.ad_requests;
        })
        .catch(error => {
          console.error("Error fetching ad requests:", error);
        });
    },
    deleteAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      axios
        .delete(`http://127.0.0.1:5000/delete_ad_request/${adRequestId}`, {
          headers: { 'Authentication-Token': token }
        })
        .then(() => {
          this.adRequests = this.adRequests.filter(adRequest => adRequest.id !== adRequestId);
        })
        .catch(error => {
          console.error("Error deleting ad request:", error);
        });
    }
  }
};
</script>

<style scoped>
/* Add your styling here */
</style>
