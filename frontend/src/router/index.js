import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../views/SignIn.vue'; // Make sure this path is correct
import AdminDashboard from '../views/AdminDashboard.vue'; // Make sure this path is correct
import AdminSponsor from '../views/AdminSponsor.vue';
import AdminCampaigns from '../views/AdminCampaign.vue';
import AdminInfluencers from '../views/AdminInfluencer.vue';
import InfluencerDashboard from '../views/InfluencerDashboard.vue';
import SponsorDashboard from '../views/SponsorDashboard.vue'; // Import SponsorDashboard component
import SponsorCampaigns from '../views/SponsorCampaign.vue'; // Import SponsorCampaigns component
import createCampaign from '../views/SponsorCreateCampaign.vue'; // Import CreateCampaign component
import EditCampaign from '../views/SponsorEditCampaign.vue'; // Import EditCampaign component
import ViewAdRequests from '../views/SponsorViewAdreq.vue'; // Import ViewAdRequests component
import InfluencerSignup from '../views/InfluencerSignup.vue'; // Import InfluencerSignup component
import SponsorSignup from '../views/SponsorSignup.vue'; // Import SponsorSignup component

const routes = [
  { path: '/', name: 'home', component: SignIn },
  { path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/admin/sponsors', name: 'AdminSponsor', component: AdminSponsor },
  { path: '/admin/campaigns', name: 'AdminCampaigns', component: AdminCampaigns },
  { path: '/influencer-dashboard', name: 'InfluencerDashboard', component: InfluencerDashboard },
  { path: '/sponsor-dashboard', name: 'SponsorDashboard', component: SponsorDashboard }, // Route for SponsorDashboard
  { path: '/campaigns', name: 'SponsorCampaigns', component: SponsorCampaigns }, // Route for listing Sponsor's campaigns
  { path: '/create-campaign', name: 'createCampaign', component: createCampaign }, // Route for creating a new campaign
  { path: '/edit-campaign/:campaignId', name: 'EditCampaign', component: EditCampaign, props: true }, // Route for editing a campaign
  { path: '/view-ad-requests/:campaignId', name: 'ViewAdRequests', component: ViewAdRequests, props: true }, // Route for viewing ad requests
  { path: '/admin/influencers', name: 'AdminInfluencers', component: AdminInfluencers },
  { path: '/register-influencer', name: 'InfluencerSignup', component: InfluencerSignup }, // Route for InfluencerSignup
  { path: '/register-sponsor', name: 'SponsorSignup', component: SponsorSignup } // Route for SponsorSignup
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
