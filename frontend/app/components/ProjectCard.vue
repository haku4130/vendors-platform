<template>
  <UCard class="rounded-2xl shadow-md flex flex-col justify-between">
    <UUser
      :name="item.owner.company_name"
      :description="item.owner.full_name"
      :avatar="{
        src: item.owner.logo_url || undefined,
        icon: 'i-lucide-camera',
        class: 'rounded-lg border border-black',
      }"
      :to="`/companies/${item.owner.id}`"
      target="_blank"
      size="3xl"
    />

    <div v-if="item.owner.rating" class="flex items-center gap-1 mt-3">
      <span class="text-sm font-semibold">{{
        item.owner.rating.toFixed(1)
      }}</span>
      <StarRating :rating="item.owner.rating" />
      <span class="text-sm text-muted">({{ item.owner.ratingCount }})</span>
    </div>
    <div v-else class="flex items-center mt-3">
      <span class="text-sm font-semibold">No rating yet</span>
    </div>

    <span class="flex w-full py-1 rounded-sm text-lg font-semibold">
      {{ item.title }}
    </span>

    <USeparator />

    <div class="my-4 space-y-3">
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

    <USeparator />

    <UButton
      label="View Project Brief"
      class="w-full justify-center mt-4"
      :to="`/dashboard/projects/${item.id}/${toUrlPostfix}`"
    />
  </UCard>
</template>

<script setup lang="ts">
import type { ProjectPublic } from '~/generated/api';

const { toUrlPostfix = '' } = defineProps<{
  item: ProjectPublic;
  toUrlPostfix?: string;
}>();
</script>
