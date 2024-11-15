import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../views/SignIn.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import AdminSponsor from '../views/AdminSponsor.vue';
import AdminCampaigns from '../views/AdminCampaign.vue';
import AdminInfluencers from '../views/AdminInfluencer.vue';
import InfluencerDashboard from '../views/InfluencerDashboard.vue';
import SponsorDashboard from '../views/SponsorDashboard.vue';
import SponsorCampaigns from '../views/SponsorCampaign.vue';
import CreateCampaign from '../views/SponsorCreateCampaign.vue';
import EditCampaign from '../views/SponsorEditCampaign.vue';
import ViewAdRequests from '../views/SponsorViewAdreq.vue';
import InfluencerSignup from '../views/InfluencerSignup.vue';
import SponsorSignup from '../views/SponsorSignup.vue';
import SponsorFindInf from '../views/SponsorFindinf.vue';
import SendAdRequest from '../views/SponsorSendAdreq.vue';
import SponsorUpdateadreq from '../views/SponsorUpdateadreq.vue';
import InfluencerAdreq from '../views/InfluencerAdreq.vue';
import InfluencerNegotiateAdreq from '../views/InfluencerNegotiateAdreq.vue';
import InfluencerFindCampaigns from '../views/InfluencerFindCampaign.vue';
import InfluencerSendAdRequest from '../views/InfluencerSendadreq.vue';
import InfluencerEditProfile from '../views/InfluencerEditProfile.vue'; // Import InfluencerEditProfile

const routes = [
  { path: '/', name: 'home', component: SignIn },
  { path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/admin/sponsors', name: 'AdminSponsor', component: AdminSponsor },
  { path: '/admin/campaigns', name: 'AdminCampaigns', component: AdminCampaigns },
  { path: '/influencer-dashboard', name: 'InfluencerDashboard', component: InfluencerDashboard },
  { path: '/sponsor-dashboard', name: 'SponsorDashboard', component: SponsorDashboard },
  { path: '/campaigns', name: 'SponsorCampaigns', component: SponsorCampaigns },
  { path: '/create-campaign', name: 'CreateCampaign', component: CreateCampaign },
  { path: '/edit-campaign/:campaignId', name: 'EditCampaign', component: EditCampaign, props: true },
  { path: '/view-ad-requests/:campaignId', name: 'ViewAdRequests', component: ViewAdRequests, props: true },
  { path: '/admin/influencers', name: 'AdminInfluencers', component: AdminInfluencers },
  { path: '/register-influencer', name: 'InfluencerSignup', component: InfluencerSignup },
  { path: '/register-sponsor', name: 'SponsorSignup', component: SponsorSignup },
  { path: '/find-influencers', name: 'SponsorFindInf', component: SponsorFindInf },
  {
    path: '/send-ad-request/:influencerId',
    name: 'SponsorSendAdreq',
    component: SendAdRequest,
    props: route => ({ influencerId: parseInt(route.params.influencerId), influencerName: route.query.name })
  },
  {
    path: '/edit-ad-request/:campaignId/:adRequestId',
    name: 'SponsorUpdateadreq',
    component: SponsorUpdateadreq,
    props: true
  },
  {
    path: '/influencer/ad-requests/:influencerId',
    name: 'InfluencerAdreq',
    component: InfluencerAdreq,
    props: true
  },
  {
    path: '/influencer/negotiate-ad-request/:adRequestId',
    name: 'InfluencerNegotiateAdRequest',
    component: InfluencerNegotiateAdreq,
    props: true
  },
  {
    path: '/public-campaigns/:influencerId',
    name: 'InfluencerFindCampaigns',
    component: InfluencerFindCampaigns,
    props: true  // This passes `influencerId` as a prop to the component
  },
  {
    path: '/influencer/send-ad-request/:campaignId',
    name: 'InfluencerSendAdRequest',
    component: InfluencerSendAdRequest,
    props: route => ({
      campaignId: parseInt(route.params.campaignId),
      campaignName: route.query.name,
      influencerId: parseInt(route.query.influencerId)
    })
  },
  {
    path: '/influencer/edit-profile',
    name: 'InfluencerEditProfile',
    component: InfluencerEditProfile
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
