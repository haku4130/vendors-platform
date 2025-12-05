<template>
  <div class="space-y-6">
    <div ref="listEl" class="space-y-4">
      <VendorCard
        v-for="vendor in vendors"
        :key="vendor.id"
        :vendor="vendor"
        :current-project-id="projectId"
      />
      <div v-if="loading">Loading...</div>
      <div v-else-if="!vendors.length">
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
import { projectsGetProjectRequests } from '~/generated/api';
import type {
  VendorProfilePublic,
  RequestInitiator,
  RequestStatus,
} from '~/generated/api';

const { projectId } = defineProps<{
  projectId: string;
}>();

const listEl = ref<HTMLElement | null>(null);
const vendors = ref<VendorProfilePublic[]>([]);
const loading = ref(false);
const total = ref<number | null>(null);

const toast = useToast();

async function loadMore() {
  if (loading.value) return;
  loading.value = true;

  const offset = vendors.value.length;
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
    vendors.value.push(...res.data.result.map((req) => req.vendor_profile));
    total.value = res.data.total;
  }

  loading.value = false;
}

useInfiniteScroll(listEl, loadMore, {
  distance: 100,
  canLoadMore: () =>
    total.value === null || vendors.value.length < (total.value ?? 0),
});
</script>
