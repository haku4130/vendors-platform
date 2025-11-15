<template>
  <AuthFormContainer class="max-w-md">
    <h2 class="text-xl font-semibold mb-6 text-gray-800">
      How will you use the platform?
    </h2>

    <div class="space-y-4 mb-8">
      <button
        v-for="(option, index) in options"
        :key="index"
        :class="[
          'w-full border rounded-lg p-4 text-left transition hover:bg-orange-200 active:bg-orange-200/70 space-y-2',
          selected === option.value
            ? 'bg-orange-200 border-black'
            : 'bg-transparent border-gray-600',
        ]"
        @click="selectOption(option.value)"
      >
        <p class="font-bold text-gray-800">{{ option.title }}</p>
        <p class="text-sm text-gray-600">{{ option.description }}</p>
      </button>
    </div>

    <UButton
      variant="solid"
      color="warning"
      size="lg"
      label="Continue"
      class="font-semibold justify-center py-2 px-10 rounded-lg mb-3"
      :disabled="!selected"
      @click="onContinue"
    />

    <p class="text-sm text-gray-800">
      Have an account?
      <NuxtLink
        to="/sign-in"
        class="font-semibold underline hover:text-gray-900"
      >
        Sign In
      </NuxtLink>
    </p>
  </AuthFormContainer>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

type Choice = 'vendor' | 'client' | null;

const selected = ref<Choice>(null);
const router = useRouter();

const options = [
  {
    value: 'client' as Choice,
    title: 'Hire a business partner',
    description:
      'I want to find and hire a provider to help our company achieve our goals.',
  },
  {
    value: 'vendor' as Choice,
    title: 'Get listed on the platform',
    description:
      "I want to sell my business' services and boost visibility for my brand.",
  },
];

function selectOption(option: Choice) {
  selected.value = option;
}

function onContinue() {
  if (!selected.value) return;
  // send to server
  router.push('/dashboard');
}
</script>
