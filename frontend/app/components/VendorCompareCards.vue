<template>
  <div class="space-y-6">
    <div ref="listEl" class="space-y-4">
      <VendorCard
        v-for="request in requests"
        :key="request.id"
        :request-id="request.id"
        :vendor="request.vendor_profile"
        :incoming="incoming"
        :current-project-id="projectId"
        :initially-shortlisted="
          shortlistedVendorIds.has(request.vendor_profile.id)
        "
      />
      <div v-if="loading">Loading...</div>
      <div v-else-if="!requests.length">
        <UEmpty
          icon="i-lucide-hourglass"
          title="Awaiting vendor requests"
          description="We’ll list their requests here as soon as they come in."
          class="w-fit mx-auto"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core';
import {
  projectsGetProjectRequests,
  shortlistGetShortlistedVendors,
} from '~/generated/api';
import type {
  RequestInitiator,
  RequestStatus,
  ProjectRequestPublicVendorFull,
} from '~/generated/api';

const { projectId, incoming } = defineProps<{
  projectId: string;
  incoming?: boolean;
}>();

const listEl = ref<HTMLElement | null>(null);
const requests = ref<ProjectRequestPublicVendorFull[]>([]);
const loading = ref(false);
const total = ref<number | null>(null);
const shortlistedVendorIds = ref<Set<string>>(new Set());

const toast = useToast();

async function loadMore() {
  if (loading.value) return;
  loading.value = true;

  const offset = requests.value.length;
  const res = await projectsGetProjectRequests({
    path: {
      project_id: projectId,
    },
    query: {
      initiator: 'vendor' as RequestInitiator,
      request_status: 'sent' as RequestStatus,
      skip: offset,
      limit: 5,
    },
  });

  if (res.error) {
    toast.add({
      title: "Can't get vendors",
      description: extractErrorMessage(res.error),
      color: 'error',
    });
  } else {
    requests.value.push(...res.data.result);
    total.value = res.data.total;
  }

  loading.value = false;
}

async function loadShortlistedVendors() {
  const res = await shortlistGetShortlistedVendors({
    path: {
      project_id: projectId,
    },
  });

  if (!res.error && res.data) {
    shortlistedVendorIds.value = new Set(res.data.map((v) => v.id));
  }
}

useInfiniteScroll(listEl, loadMore, {
  distance: 100,
  canLoadMore: () =>
    total.value === null || requests.value.length < (total.value ?? 0),
});

onMounted(() => {
  loadShortlistedVendors();
});
</script>
