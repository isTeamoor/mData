import { createRouter, createWebHistory } from "vue-router";

import StartPage from "@/sections/Start Page.vue";
//import WorkOrders from "@/sections/Work Orders.vue";

const routes = [
  {
    path: "/s-Curve",
    name: "s-Curve",
    component: () => import("@/sections/sCurve.vue"),
  },
  {
    path: "/work orders",
    name: "work-orders",
    component: () => import("@/sections/Work Orders.vue"),
  },

  {
    path: "/startPage",
    name: "start-page",
    component: StartPage,
  },
  /*{
    path: "/plan-fact/:id/:section",
    name: "plan-fact",
    component: () => import("@/sections/Work Orders/PlanFact.vue"),
  },*/
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
