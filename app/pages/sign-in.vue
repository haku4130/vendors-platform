<template>
  <div class="flex items-center justify-center px-8 py-6">
    <div
      class="bg-[#F7A86B] rounded-xl shadow-md p-8 w-full max-w-md text-center"
    >
      <!-- Заголовок -->
      <h2 class="text-xl font-semibold mb-6">
        How will you use the platform today?
      </h2>

      <!-- Опции -->
      <div class="space-y-4 mb-6">
        <button
          v-for="(option, index) in options"
          :key="index"
          :class="[
            'w-full border rounded-lg p-4 text-left transition',
            selected === option.value
              ? 'bg-orange-200 border-black'
              : 'bg-transparent border-gray-400 hover:bg-orange-200',
          ]"
          @click="selectOption(option.value)"
        >
          <p class="font-bold text-gray-900">{{ option.title }}</p>
          <p class="text-sm text-gray-800">{{ option.description }}</p>
        </button>
      </div>

      <!-- Кнопка Continue -->
      <UButton
        color=""
        size="lg"
        label="Continue"
        class="font-semibold bg-[#8B2E2E] hover:bg-[#A63B3B] text-white justify-center py-2 px-10 rounded-lg mb-3"
        :disabled="!selected"
        @click="onContinue"
      />

      <!-- Ссылка Sign In -->
      <p class="text-sm text-gray-800">
        Have an account?
        <NuxtLink
          to="/login"
          class="font-semibold underline hover:text-gray-900"
        >
          Sign In
        </NuxtLink>
      </p>
    </div>
  </div>
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
      'I want to sell my business’ services and boost visibility for my brand.',
  },
];

function selectOption(option: Choice) {
  selected.value = option;
}

function onContinue() {
  if (!selected.value) return;
  if (selected.value === 'client') {
    router.push('/register-client');
  } else if (selected.value === 'vendor') {
    router.push('/register-vendor');
  }
}
</script>
