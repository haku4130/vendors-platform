<template>
  <DashboardShortlistSection />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'company-only'],
});
</script>
