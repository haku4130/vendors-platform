<template>
  <UContainer class="space-y-4">
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      @click="navigateTo('/dashboard/projects')"
    >
      {{ $t("proposal.back") }}
    </UButton>

    <RecommendationBanner />

    <h1 class="text-center text-2xl font-semibold">
      {{ $t("explore.title") }}
    </h1>

    <VendorSelectionCards :project-id="$route.params.project_id" />
  </UContainer>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard", middleware: ["auth", "company-only"] });
</script>
