<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <div v-if="loading" class="flex justify-center items-center min-h-[400px]">
      <div class="text-center">
        <UIcon
          name="i-lucide-loader-2"
          class="w-8 h-8 animate-spin mx-auto mb-4"
        />
        <p class="text-muted">Loading vendor profile...</p>
      </div>
    </div>

    <UEmpty
      v-else-if="error"
      icon="i-lucide-alert-circle"
      title="Vendor not found"
      description="The vendor you are looking for does not exist."
      :actions="[
        {
          icon: 'i-lucide-arrow-left',
          label: 'Go to Dashboard',
          to: '/dashboard',
        },
      ]"
      class="w-fit mx-auto"
    />

    <VendorProfilePage v-else-if="vendor" :vendor="vendor" />
  </div>
</template>

<script setup lang="ts">
import type { VendorProfilePublic } from '~/generated/api';
import { vendorsGetVendorProfile } from '~/generated/api';

definePageMeta({
  layout: 'default',
});

const route = useRoute();
const vendorId = route.params.id as string;

const vendor = ref<VendorProfilePublic | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

async function loadVendorProfile() {
  loading.value = true;
  error.value = null;

  const res = await vendorsGetVendorProfile({
    path: {
      vendor_profile_id: vendorId,
    },
  });

  loading.value = false;

  if (res.error) {
    if (res.response?.status === 404) {
      error.value = 'Vendor profile not found';
    } else {
      error.value = extractErrorMessage(
        res.error,
        'Failed to load vendor profile',
      );
    }
    return;
  }

  vendor.value = res.data;
}

onMounted(() => {
  loadVendorProfile();
});
</script>
