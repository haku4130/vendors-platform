<template>
  <UPageGrid
    class="sm:grid-cols-1 lg:grid-cols-2 xl:grid-cols-2 2xl:grid-cols-3 gap-4"
  >
    <MyProjectCard v-for="item in items" :key="item.id" :item="item" />
  </UPageGrid>
</template>

<script setup lang="ts">
import type { ProjectPublic } from '~/generated/api';

defineProps<{
  items: ProjectPublic[];
}>();
</script>
