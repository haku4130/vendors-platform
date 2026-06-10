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
        <div v-else-if="incomingRequests.length" class="p-4 sm:p-6">
          <RequestGrid
            ref="incomingRequestsEl"
            :items="incomingRequests"
            to-url-postfix="incoming-request"
          />
        </div>
        <UEmpty
          v-else
          icon="i-lucide-hourglass"
          :title="$t('dashboard.vendorSection.empty.incomingTitle')"
          :description="$t('dashboard.vendorSection.empty.incomingDesc')"
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
        <div v-else-if="exploreProjects.length" class="p-4 sm:p-6">
          <ProjectGrid
            ref="exploreProjectsEl"
            :items="exploreProjects"
            to-url-postfix="proposal"
          />
        </div>
        <UEmpty
          v-else
          icon="i-lucide-hourglass"
          :title="$t('dashboard.vendorSection.empty.findTitle')"
          :description="$t('dashboard.vendorSection.empty.findDesc')"
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
            <UIcon
              name="i-lucide-loader-2"
              class="w-8 h-8 animate-spin text-muted"
            />
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
            :title="$t('dashboard.vendorSection.empty.proposalsTitle')"
            :description="$t('dashboard.vendorSection.empty.proposalsDesc')"
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
        <div v-else-if="archivedProjects.length" class="p-4 sm:p-6">
          <ProjectGrid ref="archivedProjectsEl" :items="archivedProjects" />
        </div>
        <UEmpty
          v-else
          icon="i-lucide-archive"
          :title="$t('dashboard.vendorSection.empty.archiveTitle')"
          :description="$t('dashboard.vendorSection.empty.archiveDesc')"
          class="w-fit mx-auto my-8 max-w-4/5"
        />
      </template>
    </UTabs>
  </div>
</template>

<script setup lang="ts">
import { useInfiniteScroll, useBreakpoints } from "@vueuse/core";
import {
  vendorsGetIncomingRequestsForVendor,
  vendorsGetAvailableProjectsForVendor,
  vendorsGetMyProposals,
  vendorsGetMyArchivedProjects,
} from "~/generated/api";
import type {
  ProjectPublic,
  ProjectRequestPublicProjectFull,
} from "~/generated/api";

const { t } = useI18n();

const incomingRequestsEl = useTemplateRef("incomingRequestsEl");
const incomingRequests = ref<ProjectRequestPublicProjectFull[]>([]);
const totalIncoming = ref<number | null>(null);
const loadingIncoming = ref(false);

const exploreProjectsEl = useTemplateRef("exploreProjectsEl");
const exploreProjects = ref<ProjectPublic[]>([]);
const totalExplore = ref<number | null>(null);
const loadingExplore = ref(false);

const proposalsEl = useTemplateRef("proposalsEl");
const proposals = ref<ProjectRequestPublicProjectFull[]>([]);
const totalProposals = ref<number | null>(null);
const loadingProposals = ref(false);
const proposalStatus = ref<"sent" | "accepted" | "declined" | null>(null);

const archivedProjectsEl = useTemplateRef("archivedProjectsEl");
const archivedProjects = ref<ProjectPublic[]>([]);
const totalArchived = ref<number | null>(null);
const loadingArchived = ref(false);

const toast = useToast();

const proposalFilters = computed(() => [
  { label: t("dashboard.vendorSection.filters.all"), value: null },
  { label: t("dashboard.vendorSection.filters.sent"), value: "sent" as const },
  {
    label: t("dashboard.vendorSection.filters.accepted"),
    value: "accepted" as const,
  },
  {
    label: t("dashboard.vendorSection.filters.declined"),
    value: "declined" as const,
  },
]);

function setProposalFilter(val: "sent" | "accepted" | "declined" | null) {
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
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(res.error),
      color: "error",
    });
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
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(res.error),
      color: "error",
    });
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
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(res.error),
      color: "error",
    });
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
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(res.error),
      color: "error",
    });
  } else {
    archivedProjects.value.push(...res.data.result);
    totalArchived.value = res.data.total;
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
useInfiniteScroll(proposalsEl, loadMoreProposals, {
  distance: 10,
  canLoadMore: () =>
    totalProposals.value === null ||
    proposals.value.length < (totalProposals.value ?? 0),
});
useInfiniteScroll(archivedProjectsEl, loadMoreArchived, {
  distance: 10,
  canLoadMore: () =>
    totalArchived.value === null ||
    archivedProjects.value.length < (totalArchived.value ?? 0),
});

onMounted(() => {
  loadMoreIncoming();
  loadMoreExplore();
  loadMoreProposals();
  loadMoreArchived();
});

const route = useRoute();
const router = useRouter();

const VALID_TABS = ["incoming", "search", "proposals", "archive"];

const activeTab = computed({
  get() {
    const tab = route.query.tab as string;
    return VALID_TABS.includes(tab) ? tab : "search";
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
      label: isSmallScreen
        ? t("dashboard.vendorSection.tabs.incomingShort")
        : t("dashboard.vendorSection.tabs.incoming"),
      icon: "i-lucide-inbox",
      slot: "incoming",
      value: "incoming",
    },
    {
      label: isSmallScreen
        ? t("dashboard.vendorSection.tabs.findShort")
        : t("dashboard.vendorSection.tabs.find"),
      icon: "i-lucide-compass",
      slot: "search",
      value: "search",
    },
    {
      label: isSmallScreen
        ? t("dashboard.vendorSection.tabs.proposalsShort")
        : t("dashboard.vendorSection.tabs.proposals"),
      icon: "i-lucide-file-text",
      slot: "proposals",
      value: "proposals",
    },
    {
      label: t("dashboard.vendorSection.tabs.archive"),
      icon: "i-lucide-archive",
      slot: "archive",
      value: "archive",
    },
  ];
});
</script>
