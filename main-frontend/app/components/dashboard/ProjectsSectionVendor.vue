<template>
  <div class="overflow-scroll">
    <UTabs
      :items="tabs"
      variant="link"
      class="w-full"
      :ui="{ trigger: 'grow', list: 'sticky top-0 bg-white z-10' }"
    >
      <template #incoming>
        <UContainer class="flex justify-center">
          <ProjectGrid
            ref="listEl"
            :items="projects"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
      </template>

      <template #search> search </template>
    </UTabs>
  </div>
</template>

<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core';
import { vendorsGetIncomingRequestsForVendor } from '~/generated/api';
import type { ProjectPublic } from '~/generated/api';

const listEl = ref<HTMLElement | null>(null);
const projects = ref<ProjectPublic[]>([]);
const loading = ref(false);
const total = ref<number | null>(null);

const toast = useToast();

async function loadMore() {
  if (loading.value) return;
  loading.value = true;

  const offset = projects.value.length;
  const res = await vendorsGetIncomingRequestsForVendor({
    query: {
      skip: offset,
      limit: 5,
    },
  });

  if (res.error) {
    toast.add({
      title: "Can't get incoming projects",
      description: extractErrorMessage(res.error),
      color: 'error',
    });
  } else {
    projects.value.push(...res.data.map((req) => req.project));
    total.value = res.total;
  }

  loading.value = false;
}

useInfiniteScroll(listEl, loadMore, {
  distance: 100,
  canLoadMore: () =>
    total.value === null || projects.value.length < (total.value ?? 0),
});

const tabs = [
  {
    label: 'Incoming Projects',
    icon: 'i-lucide-inbox',
    slot: 'incoming',
  },
  {
    label: 'Find a Project',
    icon: 'i-lucide-compass',
    slot: 'search',
  },
];
</script>
