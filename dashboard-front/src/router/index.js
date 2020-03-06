import Vue from 'vue'
import VueRouter from 'vue-router'
import GeneralStats from '../views/GeneralStats.vue'
import InDepth from "../views/InDepth";
import LivePerformance from '../views/LivePerformance'
import TestPerformance from "../views/TestPerformance";


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
    path: '/live-performance',
    name: 'LivePerformance',
    component: LivePerformance
  },
  {
    path: '/test-performance',
    name: 'TestPerformance',
    component: TestPerformance
  }
];

const router = new VueRouter({
  mode: 'hash',
  routes
});

export default router
