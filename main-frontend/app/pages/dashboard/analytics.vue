<template>
  <UEmpty
    icon="i-lucide-construction"
    title="That page is under construction"
    description="We are working hard to bring you this feature soon."
  />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'vendor-only'],
});
</script>
