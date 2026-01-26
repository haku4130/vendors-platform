<template>
  <div class="space-y-6">
    <div ref="listEl" class="space-y-4">
      <VendorCard
        v-for="vendor in vendors"
        :key="vendor.id"
        :vendor="vendor"
        :current-project-id="projectId"
        :request-id="''"
        :initially-shortlisted="shortlistedVendorIds.has(vendor.id)"
      />
      <div v-if="loading" class="flex items-center justify-center gap-2">
        <UIcon
          name="i-lucide-loader-2"
          class="w-6 h-6 animate-spin text-muted"
        />
        <span class="text-muted">Loading...</span>
      </div>
      <div v-else-if="!vendors.length">
        <UEmpty
          icon="i-lucide-search-x"
          title="No matching vendors found"
          description="However, vendors have received your request. Their responses will appear soon."
          class="w-fit mx-auto"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core';
import {
  projectsGetMatchingVendors,
  shortlistGetShortlistedVendors,
} from '~/generated/api';
import type { VendorProfilePublic } from '~/generated/api';

const { projectId } = defineProps<{
  projectId: string;
}>();

const listEl = ref<HTMLElement | null>(null);
const vendors = ref<VendorProfilePublic[]>([]);
const loading = ref(false);
const total = ref<number | null>(null);
const shortlistedVendorIds = ref<Set<string>>(new Set());

const toast = useToast();

async function loadMore() {
  if (loading.value) return;
  loading.value = true;

  const offset = vendors.value.length;
  const res = await projectsGetMatchingVendors({
    path: {
      project_id: projectId,
    },
    query: {
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
    vendors.value.push(...res.data.result);
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

function handleShortlistChanged(vendorId: string, isAdded: boolean) {
  if (isAdded) {
    shortlistedVendorIds.value.add(vendorId);
  } else {
    shortlistedVendorIds.value.delete(vendorId);
  }
}

useInfiniteScroll(listEl, loadMore, {
  distance: 100,
  canLoadMore: () =>
    total.value === null || vendors.value.length < (total.value ?? 0),
});

onMounted(() => {
  loadShortlistedVendors();
});
</script>
