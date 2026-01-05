<template>
  <div>
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      @click="navigateTo('/dashboard/projects')"
    >
      Back
    </UButton>

    <ExistingProjectDetail :project-id="$route.params.project_id" />

    <div class="flex justify-end mt-6">
      <div v-if="!alreadyProcessed" class="flex gap-2">
        <UButton variant="solid" size="lg" @click="handleProjectAccept">
          Accept
        </UButton>
        <UButton size="lg" @click="handleProjectDeny"> Deny </UButton>
      </div>

      <div v-else>
        <UButton disabled>
          {{ alreadyProcessed }}
        </UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { requestsAcceptProject, requestsDeclineProject } from '~/generated/api';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'vendor-only'],
});

const route = useRoute();
const alreadyProcessed = ref();
const toast = useToast();

async function handleProjectAccept() {
  const res = await requestsAcceptProject({
    path: {
      request_id: route.params.request_id as string,
    },
  });

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to accept request'),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Request accepted!',
    description: 'The company has been notified.',
    color: 'success',
  });
  alreadyProcessed.value = 'Accepted';
}

async function handleProjectDeny() {
  const res = await requestsDeclineProject({
    path: {
      request_id: route.params.request_id as string,
    },
  });

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to decline request'),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Request declined',
    description: 'The company has been notified.',
    color: 'success',
  });
  alreadyProcessed.value = 'Denied';
}
</script>
