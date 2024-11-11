import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../views/SignIn.vue'; // Make sure this path is correct
import AdminDashboard from '../views/AdminDashboard.vue'; // Make sure this path is correct
import SponsorDashboard from '../views/SponsorDashboard.vue'; // Make sure this path is correct
import InfluencerDashboard from '../views/InfluencerDashboard.vue';
//import SponsorSignup from '../views/SponsorSignup.vue';

  const routes = [
    { path: '/', name: 'home', component: SignIn },
    { path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard },
    { path: '/sponsor-dashboard', name: 'SponsorDashboard', component: SponsorDashboard },
    { path: '/influencer-dashboard', name: 'InfluencerDashboard', component: InfluencerDashboard }
  ];

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
  export default router;