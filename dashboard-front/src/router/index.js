import Vue from 'vue'
import VueRouter from 'vue-router'
import GeneralStats from '../views/GeneralStats.vue'
import InDepth from "../views/InDepth";
import ModelPerformance from '../views/ModelPerformance'


Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'GeneralStats',
    component: GeneralStats
  },
  {
    path: '/in-depth-analysis/:serial?',
    name: 'InDepth',
    component: InDepth
  },
  {
    path: '/model-performance',
    name: 'ModelPerformance',
    component: ModelPerformance
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router
