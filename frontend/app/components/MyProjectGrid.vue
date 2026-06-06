<template>
  <div class="grid lg:grid-cols-2 xl:grid-cols-2 2xl:grid-cols-3 gap-4">
    <MyProjectCard v-for="item in items" :key="item.id" :item="item" />
  </div>
</template>

<script setup lang="ts">
import type { ProjectWithIncomingCount } from "~/generated/api";

defineProps<{
  items: ProjectWithIncomingCount[];
}>();
</script>
