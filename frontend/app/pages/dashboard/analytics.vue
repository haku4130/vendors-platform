<template>
  <UEmpty
    icon="i-lucide-construction"
    :title="$t('dashboard.underConstruction.title')"
    :description="$t('dashboard.underConstruction.description')"
  />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'vendor-only'],
});
</script>
