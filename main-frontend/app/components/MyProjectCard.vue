<template>
  <UCard class="rounded-2xl shadow-md">
    <template #header>
      <span class="flex w-full py-1 rounded-sm text-xl font-semibold">
        {{ item.title }}
      </span>
    </template>

    <template #default>
      <div class="space-y-3">
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-tag" class="w-4 h-4" />
          <span>${{ item.budget }}</span>
        </div>

        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-clock" class="w-4 h-4" />
          <span>{{ item.start_date }}</span>
        </div>

        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-map-pin" class="w-4 h-4" />
          <span>{{ item.location ?? 'No preference' }}</span>
        </div>
      </div>
    </template>

    <template #footer>
      <div class="flex w-full gap-2">
        <UButton
          label="Explore Vendors"
          class="w-full justify-center"
          :to="`/dashboard/projects/${item.id}`"
        />
        <UButton
          label="Compare Quotes"
          class="w-full justify-center"
          variant="solid"
          :to="`/dashboard/projects/${item.id}`"
        />
      </div>
    </template>
  </UCard>
</template>

<script setup lang="ts">
import type { ProjectPublic } from '~/generated/api';

defineProps<{ item: ProjectPublic }>();
</script>
