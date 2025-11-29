<template>
  <UPageGrid class="lg:grid-cols-2 xl:grid-cols-3">
    <ProjectCard v-for="item in items" :key="item.id" :item="item" />
  </UPageGrid>
</template>

<script setup lang="ts">
import type { ProjectPublic } from '~/generated/api';

defineProps<{
  items: ProjectPublic[];
}>();
</script>
