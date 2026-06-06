<template>
  <div
    class="flex flex-col bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow overflow-hidden"
  >
    <div class="p-5 flex-1 space-y-3">
      <NuxtLink :to="`/dashboard/projects/${item.id}`" class="block group">
        <h3
          class="font-semibold text-base leading-snug line-clamp-2 group-hover:text-blue-600 transition-colors"
        >
          {{ item.title }}
        </h3>
      </NuxtLink>

      <div v-if="item.services?.length">
        <span
          v-for="svc in item.services.slice(0, 3)"
          :key="svc.id"
          class="inline-block mr-1 mb-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100"
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

      <div class="space-y-1.5 pt-1">
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <UIcon
            name="i-lucide-banknote"
            class="w-4 h-4 text-gray-400 shrink-0"
          />
          <span class="font-medium">${{ formatBudget(item.budget) }}</span>
        </div>
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <UIcon
            name="i-lucide-calendar"
            class="w-4 h-4 text-gray-400 shrink-0"
          />
          <span>{{ item.start_date }}</span>
        </div>
        <div
          v-if="item.location"
          class="flex items-center gap-2 text-sm text-gray-600"
        >
          <UIcon
            name="i-lucide-map-pin"
            class="w-4 h-4 text-gray-400 shrink-0"
          />
          <span>{{ item.location }}</span>
        </div>
      </div>
    </div>

    <div class="mt-auto px-5 pb-5 pt-3 border-t border-gray-100 space-y-2">
      <div
        v-if="item.is_archived"
        class="flex items-center gap-2 text-sm text-gray-400"
      >
        <UIcon name="i-lucide-archive" class="w-4 h-4" />
        <span>В архиве</span>
      </div>

      <template v-else-if="item.vendor_profile">
        <div
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-green-50 border border-green-100"
        >
          <UIcon
            name="i-lucide-circle-check"
            class="w-4 h-4 text-green-600 shrink-0"
          />
          <span class="text-sm font-medium text-green-700">Вендор выбран</span>
        </div>
        <UButton
          block
          variant="outline"
          color="neutral"
          trailing-icon="i-lucide-arrow-right"
          :to="`/vendors/${item.vendor_profile.id}`"
        >
          Посмотреть вендора
        </UButton>
      </template>

      <template v-else>
        <div
          v-if="(item.incoming_count ?? 0) > 0"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-50 border border-amber-100"
        >
          <UIcon
            name="i-lucide-inbox"
            class="w-4 h-4 text-amber-600 shrink-0"
          />
          <span class="text-sm font-medium text-amber-700"
            >{{ item.incoming_count }}
            {{
              item.incoming_count === 1 ? "предложение" : "предложений"
            }}</span
          >
        </div>
        <div class="grid grid-cols-2 gap-2">
          <UButton
            block
            variant="outline"
            color="neutral"
            :to="`/dashboard/projects/${item.id}/explore`"
          >
            Найти вендоров
          </UButton>
          <UButton block :to="`/dashboard/projects/${item.id}/compare`">
            Предложения
          </UButton>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProjectWithIncomingCount } from "~/generated/api";

defineProps<{ item: ProjectWithIncomingCount }>();

function formatBudget(n: number): string {
  if (n >= 1_000_000)
    return (n / 1_000_000).toFixed(n % 1_000_000 === 0 ? 0 : 1) + "M";
  if (n >= 1_000) return (n / 1_000).toFixed(n % 1_000 === 0 ? 0 : 1) + "K";
  return n.toLocaleString("ru-RU");
}
</script>
