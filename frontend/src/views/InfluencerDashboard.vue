<template>
  <div>
    <header>
      <div class="navbar-brand">Influencer @ SPOC</div>
      <div class="user-actions">
        <router-link to="/influencer-dashboard" class="nav-link">Profile</router-link>
        <router-link :to="`/influencer/ad-requests/${influencerId}`" class="nav-link">Ad Management</router-link>
        <router-link :to="`/public-campaigns/${influencerId}`" class="nav-link">Find Campaigns</router-link>
        <button class="button logout" @click="logout">Logout</button>
      </div>
    </header>
    
    <div class="content">
      <h1>Welcome, influencer</h1>
      <p>Your influence, empowered @ SPOC</p>
      <button class="button edit-profile" @click="editProfile">Edit Profile</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InfluencerDashboard',
  data() {
    return {
      influencerId: null 
    };
  },
  created() {

    this.influencerId = localStorage.getItem('influencerId');
  },
  methods: {
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('influencerId');  
      this.$router.push('/');
    },
    editProfile() {
      this.$router.push('/influencer/edit-profile');
    }
  }
};
</script>

<style scoped>
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

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 80px); 
  text-align: center;
}

h1 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

p {
  font-size: 20px;
  color: #555;
}

.button.edit-profile {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}

.button.edit-profile:hover {
  background-color: #2980b9;
}
</style>
