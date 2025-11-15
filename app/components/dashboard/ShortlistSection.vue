<template>
  <div class="space-y-8">
    <!-- Top orange header -->
    <section class="bg-[#FFB27B] p-6 rounded-2xl">
      <h2 class="text-xl font-semibold text-gray-900">
        Solve your business challenge faster with Shortlist
      </h2>
    </section>

    <!-- How it works + Empty state -->
    <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Left: How it works -->
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold mb-6">How it works</h3>

        <UStepper
          v-model="active"
          color="neutral"
          orientation="vertical"
          :items="items"
          class="w-full"
        />
      </div>

      <!-- Right: Empty favorites message -->
      <div
        class="bg-white rounded-2xl p-6 shadow-sm flex flex-col justify-center max-h-fit"
      >
        <h3 class="text-lg font-semibold mb-4">
          You haven’t picked your favorites yet!
        </h3>
        <UButton size="xl" class="w-fit"> Find a Vendor </UButton>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { StepperItem } from '@nuxt/ui';

const items = ref<StepperItem[]>([
  {
    title: 'Start a Project',
    description: 'Create a brief describing your needs and goals.',
  },
  {
    title: 'Get Matched',
    description:
      'We’ll suggest the best-fit vendors based on your project details.',
  },
  {
    title: 'Shortlist & Decide',
    description:
      'Compare proposals, pick your favorites, and choose who to work with.',
  },
]);

const active = ref(0);

onMounted(() => {
  setInterval(() => {
    active.value = (active.value + 1) % items.value.length;
  }, 1500);
});
</script>
