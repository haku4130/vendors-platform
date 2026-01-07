<template>
  <div class="w-full max-w-5xl rounded-xl pb-8">
    <h2 class="text-2xl font-semibold">
      Select service providers to bid on your project
    </h2>
    <div class="max-w-fit mx-auto">
      <USeparator label="Or" class="my-4" />
      <p class="mb-6">
        Click “Send to Vendors” button to make your project open and you would
        just wait for proposals
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
