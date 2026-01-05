<template>
  <div>
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      @click="navigateTo('/dashboard/projects')"
    >
      Back
    </UButton>

    <ExistingProjectDetail :project-id="useRoute().params.project_id" />

    <div class="flex justify-end mt-6">
      <UButton
        :disabled="alreadySent"
        :variant="alreadySent ? 'outline' : 'solid'"
        @click="handleSendRequest"
      >
        {{ alreadySent ? 'Sent!' : 'Send a Proposal' }}
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { projectsSendProjectRequestVendor } from '~/generated/api';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'vendor-only'],
});

const alreadySent = ref(false);
const toast = useToast();

async function handleSendRequest() {
  const res = await projectsSendProjectRequestVendor({
    path: {
      project_id: useRoute().params.project_id as string,
    },
  });

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to send request'),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Proposal sent',
    description: 'The company has been notified.',
    color: 'success',
  });
  alreadySent.value = true;
}
</script>
