<template>
  <VendorRegistrationForm />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'vendor-only'],
});
</script>
