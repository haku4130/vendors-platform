<template>
  <UPageGrid class="lg:grid-cols-2 xl:grid-cols-3">
    <ProjectCard
      v-for="item in items"
      :key="item.id"
      :item="item.project"
      :to-url-postfix="`${toUrlPostfix}/${item.id}`"
    />
  </UPageGrid>
</template>

<script setup lang="ts">
import type { ProjectRequestPublicProjectFull } from '~/generated/api';

const { toUrlPostfix = '' } = defineProps<{
  items: ProjectRequestPublicProjectFull[];
  toUrlPostfix?: string;
}>();
</script>
