<template>
  <DashboardProjectsSectionCompany v-if="auth.user.value?.role === 'company'" />
  <DashboardProjectsSectionVendor v-else />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
});

const auth = useAuth();
</script>
