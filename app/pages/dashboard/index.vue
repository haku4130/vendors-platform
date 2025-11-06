<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar title="Dashboard" />
    </template>

    <!-- <template #body>
      <NuxtPage />
    </template> -->
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: () => navigateTo('/dashboard/projects'),
});
</script>
