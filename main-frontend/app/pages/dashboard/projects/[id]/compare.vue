<template>
  <UContainer>
    <VendorSelection :project-id="$route.params.id" />
  </UContainer>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'dashboard', middleware: ['auth', 'company-only'] });
</script>
