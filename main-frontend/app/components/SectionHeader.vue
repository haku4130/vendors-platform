<template>
  <div class="flex items-center gap-2 mb-2">
    <h2 class="text-lg font-bold">{{ title }}</h2>
    <UButton
      icon="material-symbols:edit-square-outline"
      variant="ghost"
      color="neutral"
      @click="$emit('edit')"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
}>();
defineEmits(['edit']);
</script>
