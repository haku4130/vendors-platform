<template>
  <div class="w-full max-w-5xl rounded-xl pb-8">
    <RecommendationBanner class="mb-4" />
    <h2 class="text-2xl font-semibold text-center">
      {{ $t("vendorSelection.title") }}
    </h2>
    <div class="max-w-fit mx-auto">
      <USeparator :label="$t('vendorSelection.or')" class="my-4" />
      <p class="mb-6">
        {{ $t("vendorSelection.hint") }}
      </p>
    </div>

    <VendorSelectionCards :project-id="projectId" />
  </div>
</template>

<script setup lang="ts">
const { projectId } = defineProps<{
  projectId: string;
}>();
</script>
