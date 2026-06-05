<template>
  <div class="max-w-3xl mx-auto w-full space-y-4">
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      color="neutral"
      @click="router.back()"
    >
      Назад
    </UButton>

    <ExistingProjectDetail :project-id="useRoute().params.project_id" />
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
});

const router = useRouter();
</script>
