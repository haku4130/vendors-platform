<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar title="Dashboard" />
    </template>

    <template #body>
      <DashboardReviewsSection />
    </template>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
});
</script>
