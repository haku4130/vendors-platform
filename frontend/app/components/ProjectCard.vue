<template>
  <div
    class="flex flex-col bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow overflow-hidden"
  >
    <!-- Header -->
    <div class="p-5 pb-4">
      <div class="flex items-center gap-3 mb-4">
        <div
          class="w-10 h-10 rounded-xl flex items-center justify-center text-white text-sm font-bold shrink-0"
          :style="{ backgroundColor: avatarColor(item.owner.company_name) }"
        >
          {{ initials(item.owner.company_name) }}
        </div>
        <div class="min-w-0">
          <NuxtLink
            :to="`/companies/${item.owner.id}`"
            target="_blank"
            class="font-semibold text-sm leading-tight truncate block hover:underline"
          >
            {{ item.owner.company_name }}
          </NuxtLink>
          <p class="text-xs text-gray-400 truncate">{{ item.owner.full_name }}</p>
        </div>

        <div class="ml-auto shrink-0">
          <div v-if="item.owner.rating" class="flex items-center gap-1">
            <UIcon name="i-lucide-star" class="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
            <span class="text-sm font-semibold">{{ item.owner.rating.toFixed(1) }}</span>
          </div>
          <span v-else class="text-xs text-gray-400">Нет оценки</span>
        </div>
      </div>

      <!-- Title -->
      <h3 class="font-semibold text-base leading-snug line-clamp-2 mb-3">
        {{ item.title }}
      </h3>

      <!-- Service tags -->
      <div v-if="item.services?.length" class="mb-3">
        <span
          v-for="svc in item.services.slice(0, 3)"
          :key="svc.id"
          class="inline-block mr-1.5 mb-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100"
        >
          {{ svc.label }}
        </span>
        <span
          v-if="item.services.length > 3"
          class="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-500"
        >
          +{{ item.services.length - 3 }}
        </span>
      </div>
    </div>

    <div class="px-5 pb-4 space-y-2">
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <UIcon name="i-lucide-banknote" class="w-4 h-4 text-gray-400 shrink-0" />
        <span class="font-medium">${{ formatBudget(item.budget) }}</span>
      </div>
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <UIcon name="i-lucide-calendar" class="w-4 h-4 text-gray-400 shrink-0" />
        <span>{{ item.start_date }}</span>
      </div>
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <UIcon name="i-lucide-map-pin" class="w-4 h-4 text-gray-400 shrink-0" />
        <span>{{ item.location ?? 'Без привязки к месту' }}</span>
      </div>
    </div>

    <!-- Footer -->
    <div class="mt-auto px-5 pb-5 pt-3 border-t border-gray-100">
      <UButton
        block
        variant="outline"
        color="primary"
        trailing-icon="i-lucide-arrow-right"
        :to="`/dashboard/projects/${item.id}/${toUrlPostfix}`"
      >
        Смотреть бриф
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProjectPublic } from '~/generated/api';

const { toUrlPostfix = '' } = defineProps<{
  item: ProjectPublic;
  toUrlPostfix?: string;
}>();

const AVATAR_COLORS = [
  '#2563eb', '#16a34a', '#9333ea', '#db2777', '#d97706',
  '#0891b2', '#dc2626', '#059669', '#7c3aed', '#0284c7',
];

function avatarColor(name: string): string {
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length];
}

function initials(name: string): string {
  return name.split(' ').slice(0, 2).map((w) => w[0]).join('').toUpperCase();
}

function formatBudget(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(n % 1_000_000 === 0 ? 0 : 1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(n % 1_000 === 0 ? 0 : 1) + 'K';
  return n.toLocaleString('ru-RU');
}
</script>
