<template>
  <div>
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      @click="navigateTo('/dashboard/projects')"
    >
      Back
    </UButton>

    <ExistingProjectDetail :project-id="useRoute().params.project_id" />
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
});
</script>
