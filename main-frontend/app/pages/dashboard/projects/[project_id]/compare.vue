<template>
  <UContainer>
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      @click="navigateTo('/dashboard/projects')"
    >
      Back
    </UButton>

    <h1 class="text-center my-5 text-2xl font-semibold">
      Select from best fit vendors for your project
    </h1>

    <VendorCompareCards :project-id="$route.params.project_id" incoming />
  </UContainer>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'dashboard', middleware: ['auth', 'company-only'] });
</script>
