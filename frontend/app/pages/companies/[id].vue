<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <div v-if="loading" class="flex justify-center items-center min-h-[400px]">
      <div class="text-center">
        <UIcon
          name="i-lucide-loader-2"
          class="w-8 h-8 animate-spin mx-auto mb-4"
        />
        <p class="text-muted">Loading company profile...</p>
      </div>
    </div>

    <UEmpty
      v-else-if="error"
      icon="i-lucide-alert-circle"
      title="Company not found"
      description="The company you are looking for does not exist."
      :actions="[
        {
          icon: 'i-lucide-arrow-left',
          label: 'Go to Dashboard',
          to: '/dashboard',
        },
      ]"
      class="w-fit mx-auto"
    />

    <CompanyProfilePage v-else-if="company" :company="company" />
  </div>
</template>

<script setup lang="ts">
import type { UserPublic } from '~/generated/api';
import { usersReadUserById } from '~/generated/api';

definePageMeta({
  layout: 'default',
});

const route = useRoute();
const companyId = route.params.id as string;

const company = ref<UserPublic | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

async function loadCompanyProfile() {
  loading.value = true;
  error.value = null;

  const res = await usersReadUserById({
    path: {
      user_id: companyId,
    },
  });

  loading.value = false;

  if (res.error) {
    if (res.response?.status === 404) {
      error.value = 'Company profile not found';
    } else {
      error.value = extractErrorMessage(
        res.error,
        'Failed to load company profile',
      );
    }
    return;
  }

  // Check if user is a company
  if (res.data.role !== 'company') {
    error.value = 'This user is not a company';
    return;
  }

  company.value = res.data;
}

onMounted(() => {
  loadCompanyProfile();
});
</script>
