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
          <RequestGrid
            ref="incomingRequestsEl"
            :items="incomingRequests"
            to-url-postfix="incoming-request"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-if="!incomingRequests.length"
          icon="i-lucide-hourglass"
          title="Awaiting companies requests"
          description="We’ll list their requests here as soon as they come in."
          class="w-fit mx-auto my-8 max-w-4/5"
        />
      </template>

      <template #search>
        <UContainer class="flex justify-center">
          <ProjectGrid
            ref="exploreProjectsEl"
            :items="exploreProjects"
            to-url-postfix="proposal"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-if="!exploreProjects.length"
          icon="i-lucide-hourglass"
          title="Awaiting companies projects"
          description="We’ll list their projects here as soon as they come in."
          class="w-fit mx-auto my-8 max-w-4/5"
        />
      </template>

      <template #accepted>
        <UContainer class="flex justify-center">
          <ProjectGrid
            ref="acceptedProjectsEl"
            :items="acceptedProjects"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-if="!acceptedProjects.length"
          icon="i-lucide-search-x"
          title="You have no active projects"
          description="We’ll list your accepted projects here as soon as they come in."
          class="w-fit mx-auto my-8 max-w-4/5"
        />
      </template>
    </UTabs>
  </div>
</template>

<script setup lang="ts">
import { useInfiniteScroll, useBreakpoints } from '@vueuse/core';
import {
  vendorsGetIncomingRequestsForVendor,
  vendorsGetAvailableProjectsForVendor,
  vendorsGetMyAcceptedProjects,
} from '~/generated/api';
import type {
  ProjectPublic,
  ProjectRequestPublicProjectFull,
} from '~/generated/api';

const incomingRequestsEl = useTemplateRef('incomingRequestsEl');
const incomingRequests = ref<ProjectRequestPublicProjectFull[]>([]);
const totalIncoming = ref<number | null>(null);

const exploreProjectsEl = useTemplateRef('exploreProjectsEl');
const exploreProjects = ref<ProjectPublic[]>([]);
const totalExplore = ref<number | null>(null);

const acceptedProjectsEl = useTemplateRef('acceptedProjectsEl');
const acceptedProjects = ref<ProjectPublic[]>([]);
const totalAccepted = ref<number | null>(null);

const toast = useToast();

async function loadMoreIncoming() {
  const offset = incomingRequests.value.length;
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
    incomingRequests.value.push(...res.data.result);
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

async function loadMoreAccepted() {
  const offset = acceptedProjects.value.length;
  const res = await vendorsGetMyAcceptedProjects({
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
    acceptedProjects.value.push(...res.data.result);
    totalAccepted.value = res.data.total;
  }
}

useInfiniteScroll(incomingRequestsEl, loadMoreIncoming, {
  distance: 10,
  canLoadMore: () =>
    totalIncoming.value === null ||
    incomingRequests.value.length < (totalIncoming.value ?? 0),
});
useInfiniteScroll(exploreProjectsEl, loadMoreExplore, {
  distance: 10,
  canLoadMore: () =>
    totalExplore.value === null ||
    exploreProjects.value.length < (totalExplore.value ?? 0),
});
useInfiniteScroll(acceptedProjectsEl, loadMoreAccepted, {
  distance: 10,
  canLoadMore: () =>
    totalAccepted.value === null ||
    acceptedProjects.value.length < (totalAccepted.value ?? 0),
});

const breakpoints = useBreakpoints({
  sm: 640,
});

const tabs = computed(() => {
  const isSmallScreen = !breakpoints.sm.value;
  return [
    {
      label: isSmallScreen ? 'Incoming' : 'Incoming Projects',
      icon: 'i-lucide-inbox',
      slot: 'incoming',
    },
    {
      label: isSmallScreen ? 'Find' : 'Find a Project',
      icon: 'i-lucide-compass',
      slot: 'search',
    },
    {
      label: isSmallScreen ? 'Accepted' : 'Accepted Projects',
      icon: 'i-lucide-clipboard-check',
      slot: 'accepted',
    },
  ];
});
</script>
