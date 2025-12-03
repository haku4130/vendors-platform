<template>
  <div>
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      @click="navigateTo('/dashboard/projects')"
    >
      Back
    </UButton>

    <ProjectDetail
      :data="project"
      :company-name="auth.user.value?.company_name || ''"
      :contact-email="auth.user.value?.email || ''"
      :contact-name="auth.user.value?.full_name || ''"
      class="max-w-3xl"
    />

    <div class="flex justify-end">
      <UButton trailing-icon="i-lucide-arrow-right" variant="solid">
        Send a Proposal
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'vendor-only'],
});

const auth = useAuth();

const route = useRoute();
const id = route.params.id;

// Временные данные для UI
const project = ref({
  projectName: 'Custom Software Development',
  servicesNeeded: ['UI/UX Design', 'Mobile Application', 'API Integration'],
  startTime: 'Within 60 days',
  budget: 25000,
  locationPreference: 'specific',
  exactLocation: 'Moscow, Russia',
  website: 'https://example.com',
  projectIntroduction: `We are Example Inc, a dedicated company focused on delivering exceptional services in our field. 
  Currently, we are facing challenges in streamlining our operations and enhancing user engagement.
  To tackle this, we are seeking the expertise of a reliable service provider who can help us develop a custom software solution tailored to our needs.`,
  questions: [
    'What is your estimated timeline?',
    'Do you have an in-house development team?',
  ],
  requirements: [
    'NDA required',
    'Weekly project updates',
    'Dedicated project manager',
  ],
});
</script>
