import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../views/SignIn.vue'; // Make sure this path is correct
import AdminDashboard from '../views/AdminDashboard.vue'; // Make sure this path is correct
import AdminSponsor from '../views/AdminSponsor.vue';
import AdminCampaigns from '../views/AdminCampaign.vue';

import AdminInfluencers from '../views/AdminInfluencer.vue';

import InfluencerDashboard from '../views/InfluencerDashboard.vue';


  const routes = [
    { path: '/', name: 'home', component: SignIn },
    { path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard },
    { path: '/admin/sponsors', name: 'AdminSponsor', component: AdminSponsor },
    { path: '/admin/campaigns', name: 'AdminCampaigns', component: AdminCampaigns },
    { path: '/influencer-dashboard', name: 'InfluencerDashboard', component: InfluencerDashboard },
    { path: '/admin/influencers', name: 'AdminInfluencers', component: AdminInfluencers }
    
  ];

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
  export default router;