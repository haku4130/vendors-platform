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
            ref="incomingProjectsEl"
            :items="incomingProjects"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-if="!incomingProjects.length"
          icon="i-lucide-hourglass"
          title="Awaiting companies requests"
          description="We’ll list their requests here as soon as they come in."
          class="w-fit mx-auto my-8"
        />
      </template>

      <template #search>
        <UContainer class="flex justify-center">
          <ProjectGrid
            ref="exploreProjectsEl"
            :items="exploreProjects"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-if="!exploreProjects.length"
          icon="i-lucide-hourglass"
          title="Awaiting companies projects"
          description="We’ll list their projects here as soon as they come in."
          class="w-fit mx-auto my-8"
        />
      </template>
    </UTabs>
  </div>
</template>

<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core';
import {
  vendorsGetIncomingRequestsForVendor,
  vendorsGetAvailableProjectsForVendor,
} from '~/generated/api';
import type { ProjectPublic } from '~/generated/api';

const incomingProjectsEl = useTemplateRef('incomingProjectsEl');
const incomingProjects = ref<ProjectPublic[]>([]);
const exploreProjectsEl = useTemplateRef('exploreProjectsEl');
const exploreProjects = ref<ProjectPublic[]>([]);
const totalIncoming = ref<number | null>(null);
const totalExplore = ref<number | null>(null);

const toast = useToast();

async function loadMoreIncoming() {
  const offset = incomingProjects.value.length;
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
    incomingProjects.value.push(...res.data.result.map((req) => req.project));
    totalIncoming.value = res.data.total;
  }
}

async function loadMoreExplore() {
  const offset = exploreProjects.value.length;
  const res = await vendorsGetAvailableProjectsForVendor({
    query: {
      skip: offset,
      limit: 5,
    },
  });

  if (res.error) {
    toast.add({
      title: "Can't get projects",
      description: extractErrorMessage(res.error),
      color: 'error',
    });
  } else {
    exploreProjects.value.push(...res.data.result);
    totalExplore.value = res.data.total;
  }
}

useInfiniteScroll(incomingProjectsEl, loadMoreIncoming, {
  distance: 10,
  canLoadMore: () =>
    totalIncoming.value === null ||
    incomingProjects.value.length < (totalIncoming.value ?? 0),
});
useInfiniteScroll(exploreProjectsEl, loadMoreExplore, {
  distance: 10,
  canLoadMore: () =>
    totalExplore.value === null ||
    exploreProjects.value.length < (totalExplore.value ?? 0),
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
