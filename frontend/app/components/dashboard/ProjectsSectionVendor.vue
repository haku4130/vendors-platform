<template>
  <div class="overflow-scroll">
    <UTabs
      v-model="activeTab"
      :items="tabs"
      variant="link"
      class="w-full"
      :ui="{ trigger: 'grow', list: 'sticky top-0 bg-white z-10' }"
    >
      <template #incoming>
        <div v-if="loadingIncoming" class="flex justify-center py-12">
          <UIcon
            name="i-lucide-loader-2"
            class="w-8 h-8 animate-spin text-muted"
          />
        </div>
        <UContainer
          v-else-if="incomingRequests.length"
          class="flex justify-center"
        >
          <RequestGrid
            ref="incomingRequestsEl"
            :items="incomingRequests"
            to-url-postfix="incoming-request"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-else
          icon="i-lucide-hourglass"
          title="Awaiting companies requests"
          description="We'll list their requests here as soon as they come in."
          class="w-fit mx-auto my-8 max-w-4/5"
        />
      </template>

      <template #search>
        <div v-if="loadingExplore" class="flex justify-center py-12">
          <UIcon
            name="i-lucide-loader-2"
            class="w-8 h-8 animate-spin text-muted"
          />
        </div>
        <UContainer
          v-else-if="exploreProjects.length"
          class="flex justify-center"
        >
          <ProjectGrid
            ref="exploreProjectsEl"
            :items="exploreProjects"
            to-url-postfix="proposal"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-else
          icon="i-lucide-hourglass"
          title="Awaiting companies projects"
          description="We'll list their projects here as soon as they come in."
          class="w-fit mx-auto my-8 max-w-4/5"
        />
      </template>

      <template #proposals>
        <div class="p-4 sm:p-6">
          <!-- Status filters -->
          <div class="flex gap-2 mb-6 flex-wrap">
            <button
              v-for="f in proposalFilters"
              :key="f.value ?? 'all'"
              :class="[
                'px-4 py-1.5 rounded-full text-sm font-medium border transition',
                proposalStatus === f.value
                  ? 'bg-primary text-white border-primary'
                  : 'bg-white text-gray-600 border-gray-300 hover:border-gray-400',
              ]"
              @click="setProposalFilter(f.value)"
            >
              {{ f.label }}
            </button>
          </div>

          <div v-if="loadingProposals" class="flex justify-center py-12">
            <UIcon name="i-lucide-loader-2" class="w-8 h-8 animate-spin text-muted" />
          </div>
          <div
            v-else-if="proposals.length"
            ref="proposalsEl"
            class="grid lg:grid-cols-2 xl:grid-cols-3 gap-4"
          >
            <ProposalCard
              v-for="proposal in proposals"
              :key="proposal.id"
              :proposal="proposal"
            />
          </div>
          <UEmpty
            v-else
            icon="i-lucide-file-text"
            title="Заявок нет"
            description="Здесь появятся ваши отклики на проекты."
            class="w-fit mx-auto my-8"
          />
        </div>
      </template>

      <template #archive>
        <div v-if="loadingArchived" class="flex justify-center py-12">
          <UIcon
            name="i-lucide-loader-2"
            class="w-8 h-8 animate-spin text-muted"
          />
        </div>
        <UContainer
          v-else-if="archivedProjects.length"
          class="flex justify-center"
        >
          <ProjectGrid
            ref="archivedProjectsEl"
            :items="archivedProjects"
            class="p-4 sm:p-6 w-full max-w-5xl"
          />
        </UContainer>
        <UEmpty
          v-else
          icon="i-lucide-archive"
          title="No archived projects"
          description="Projects you applied to that were archived will appear here."
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
  vendorsGetMyProposals,
  vendorsGetMyArchivedProjects,
} from '~/generated/api';
import type {
  ProjectPublic,
  ProjectRequestPublicProjectFull,
} from '~/generated/api';

const incomingRequestsEl = useTemplateRef('incomingRequestsEl');
const incomingRequests = ref<ProjectRequestPublicProjectFull[]>([]);
const totalIncoming = ref<number | null>(null);
const loadingIncoming = ref(false);

const exploreProjectsEl = useTemplateRef('exploreProjectsEl');
const exploreProjects = ref<ProjectPublic[]>([]);
const totalExplore = ref<number | null>(null);
const loadingExplore = ref(false);

const proposalsEl = useTemplateRef('proposalsEl');
const proposals = ref<ProjectRequestPublicProjectFull[]>([]);
const totalProposals = ref<number | null>(null);
const loadingProposals = ref(false);
const proposalStatus = ref<'sent' | 'accepted' | 'declined' | null>(null);

const archivedProjectsEl = useTemplateRef('archivedProjectsEl');
const archivedProjects = ref<ProjectPublic[]>([]);
const totalArchived = ref<number | null>(null);
const loadingArchived = ref(false);

const toast = useToast();

const proposalFilters = [
  { label: 'Все', value: null },
  { label: 'На рассмотрении', value: 'sent' as const },
  { label: 'Принято', value: 'accepted' as const },
  { label: 'Отклонено', value: 'declined' as const },
];

function setProposalFilter(val: 'sent' | 'accepted' | 'declined' | null) {
  proposalStatus.value = val;
  proposals.value = [];
  totalProposals.value = null;
  loadMoreProposals();
}

async function loadMoreIncoming() {
  if (loadingIncoming.value) return;
  loadingIncoming.value = true;
  const res = await vendorsGetIncomingRequestsForVendor({
    query: { skip: incomingRequests.value.length, limit: 5 },
  });
  loadingIncoming.value = false;
  if (res.error) {
    toast.add({ title: "Can't get incoming projects", description: extractErrorMessage(res.error), color: 'error' });
  } else {
    incomingRequests.value.push(...res.data.result);
    totalIncoming.value = res.data.total;
  }
}

async function loadMoreExplore() {
  if (loadingExplore.value) return;
  loadingExplore.value = true;
  const res = await vendorsGetAvailableProjectsForVendor({
    query: { skip: exploreProjects.value.length, limit: 5 },
  });
  loadingExplore.value = false;
  if (res.error) {
    toast.add({ title: "Can't get projects", description: extractErrorMessage(res.error), color: 'error' });
  } else {
    exploreProjects.value.push(...res.data.result);
    totalExplore.value = res.data.total;
  }
}

async function loadMoreProposals() {
  if (loadingProposals.value) return;
  loadingProposals.value = true;
  const res = await vendorsGetMyProposals({
    query: {
      skip: proposals.value.length,
      limit: 10,
      request_status: proposalStatus.value ?? undefined,
    },
  });
  loadingProposals.value = false;
  if (res.error) {
    toast.add({ title: "Can't get proposals", description: extractErrorMessage(res.error), color: 'error' });
  } else {
    proposals.value.push(...res.data.result);
    totalProposals.value = res.data.total;
  }
}

async function loadMoreArchived() {
  if (loadingArchived.value) return;
  loadingArchived.value = true;
  const res = await vendorsGetMyArchivedProjects({
    query: { skip: archivedProjects.value.length, limit: 5 },
  });
  loadingArchived.value = false;
  if (res.error) {
    toast.add({ title: "Can't get archived projects", description: extractErrorMessage(res.error), color: 'error' });
  } else {
    archivedProjects.value.push(...res.data.result);
    totalArchived.value = res.data.total;
  }
}

useInfiniteScroll(incomingRequestsEl, loadMoreIncoming, {
  distance: 10,
  canLoadMore: () => totalIncoming.value === null || incomingRequests.value.length < (totalIncoming.value ?? 0),
});
useInfiniteScroll(exploreProjectsEl, loadMoreExplore, {
  distance: 10,
  canLoadMore: () => totalExplore.value === null || exploreProjects.value.length < (totalExplore.value ?? 0),
});
useInfiniteScroll(proposalsEl, loadMoreProposals, {
  distance: 10,
  canLoadMore: () => totalProposals.value === null || proposals.value.length < (totalProposals.value ?? 0),
});
useInfiniteScroll(archivedProjectsEl, loadMoreArchived, {
  distance: 10,
  canLoadMore: () => totalArchived.value === null || archivedProjects.value.length < (totalArchived.value ?? 0),
});

onMounted(() => {
  loadMoreIncoming();
  loadMoreExplore();
  loadMoreProposals();
  loadMoreArchived();
});

const route = useRoute();
const router = useRouter();

const VALID_TABS = ['incoming', 'search', 'proposals', 'archive'];

const activeTab = computed({
  get() {
    const tab = route.query.tab as string;
    return VALID_TABS.includes(tab) ? tab : 'search';
  },
  set(val: string) {
    router.replace({ query: { ...route.query, tab: val } });
  },
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
      value: 'incoming',
    },
    {
      label: isSmallScreen ? 'Find' : 'Find a Project',
      icon: 'i-lucide-compass',
      slot: 'search',
      value: 'search',
    },
    {
      label: isSmallScreen ? 'Заявки' : 'Мои заявки',
      icon: 'i-lucide-file-text',
      slot: 'proposals',
      value: 'proposals',
    },
    {
      label: isSmallScreen ? 'Archive' : 'Archive',
      icon: 'i-lucide-archive',
      slot: 'archive',
      value: 'archive',
    },
  ];
});
</script>
