<template>
  <div
    class="border border-gray-400 rounded-lg overflow-hidden divide-y divide-gray-400 text-sm"
  >
    <div
      v-for="(item, index) in info"
      :key="index"
      class="flex justify-between px-4 py-3"
    >
      <div class="flex items-center gap-2">
        <UIcon :name="item.icon" class="text-xl text-gray-500" />
        <span class="font-bold text-gray-700">{{ item.title }}</span>
      </div>
      <div class="text-right flex flex-col items-end">
        <span class="text-gray-900">{{ item.value }}</span>
        <span class="font-semibold text-gray-900">{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  info: {
    icon: string;
    title: string;
    value: string;
    label?: string;
  }[];
}>();
</script>
