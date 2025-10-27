<template>
  <UModal
    v-model:open="open"
    title="Project Brief"
    :ui="{ header: 'bg-[#F7A86B]', footer: 'justify-between' }"
    fullscreen
  >
    <button
      class="border border-black rounded-md px-4 py-2 font-medium hover:bg-black hover:text-white transition"
    >
      Start a Project
    </button>
    <template #body>
      <div class="flex flex-col w-full h-full">
        <!-- Прогресс-бар -->
        <UProgress v-model="step" :max="totalSteps" color="neutral" />

        <!-- Основной контент -->
        <div
          class="flex-1 flex flex-col items-center justify-center px-8 py-6 text-center"
        >
          <p class="text-sm text-gray-700 mb-1">
            Step {{ step }} / {{ totalSteps }}
          </p>
          <h3 class="text-xl font-semibold text-gray-900 mb-6">
            {{ currentStep.title }}
          </h3>

          <div class="w-full max-w-xl">
            <!-- textarea -->
            <textarea
              v-if="currentStep.type === 'textarea'"
              v-model="answers[step]"
              :placeholder="currentStep.placeholder"
              class="w-full border border-gray-400 rounded-lg px-4 py-3 h-32 resize-none focus:outline-none focus:ring-2 focus:ring-gray-500"
            />

            <!-- input -->
            <input
              v-else-if="currentStep.type === 'input'"
              v-model="answers[step]"
              :placeholder="currentStep.placeholder"
              class="w-full border border-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-gray-500"
            />

            <!-- radio-like options -->
            <div
              v-else-if="currentStep.type === 'options'"
              class="flex w-fit justify-center gap-3 mx-auto"
              :class="[currentStep.optionsColumns ? 'flex-col' : 'flex-row']"
            >
              <button
                v-for="option in currentStep.options"
                :key="option"
                class="w-full min-w-fit border border-gray-600 rounded-md px-4 py-2 font-medium transition"
                :class="[
                  answers[step] === option
                    ? 'bg-gray-800 text-white border-gray-800'
                    : 'hover:bg-gray-100 text-gray-800',
                ]"
                @click="answers[step] = option"
              >
                {{ option }}
              </button>
            </div>

            <!-- input + checkbox -->
            <div
              v-else-if="currentStep.type === 'inputWithCheckbox'"
              class="flex flex-col items-center gap-2"
            >
              <input
                v-model="answers[step]"
                :placeholder="currentStep.placeholder"
                class="w-full border border-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-gray-500"
                :disabled="answers[step + '_noWebsite']"
              />
              <label class="flex items-center gap-2 text-sm text-gray-700">
                <input v-model="answers[step + '_noWebsite']" type="checkbox" />
                {{ currentStep.checkboxLabel }}
              </label>
            </div>

            <!-- company name + description -->
            <div
              v-else-if="currentStep.type === 'doubleInput'"
              class="flex flex-col gap-5 w-full"
            >
              <input
                v-model="answers[step + '_name']"
                :placeholder="currentStep.fields[0].placeholder"
                class="border border-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-gray-500"
              />
              <textarea
                v-model="answers[step + '_about']"
                :placeholder="currentStep.fields[1].placeholder"
                class="border border-gray-400 rounded-lg px-4 py-3 h-24 resize-none focus:outline-none focus:ring-2 focus:ring-gray-500"
              />
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <button
        class="px-4 py-2 border border-gray-800 rounded-md hover:bg-gray-800 hover:text-white transition disabled:opacity-50"
        :disabled="step === 1"
        @click="prevStep"
      >
        Back
      </button>
      <button
        class="px-6 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition"
        @click="nextStep"
      >
        {{ step === totalSteps ? 'Finish' : 'Next' }}
      </button>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const open = ref(false);
const step = ref(1);
const totalSteps = 6;

interface Step {
  title: string;
  type: 'input' | 'textarea' | 'options' | 'inputWithCheckbox' | 'doubleInput';
  placeholder: string;
}

const steps: Step[] = [
  {
    title: "What's your project about? What goals do you want to accomplish?",
    type: 'textarea',
    placeholder:
      'E.g., Optimize website for faster performance / Grow website traffic through targeted keyword optimization / Make my website navigation more user friendly.',
  },
  {
    title: 'What kind of company are you looking for?',
    type: 'input',
    placeholder: 'Search for SEO, web development, etc.',
  },
  {
    title: 'When would you like to start this project?',
    type: 'options',
    options: ['Within 30 days', 'Within 60 days', 'After 60+ days'],
  },
  {
    title: "What's important to you about a provider's location?",
    type: 'options',
    options: [
      'No preference — just looking for the best providers',
      'Near me for in-person collaboration',
      'I have specific countries in mind',
    ],
    optionsColumns: true,
  },
  {
    title: "What's your company's website?",
    type: 'inputWithCheckbox',
    placeholder: 'www.yourcompany.com',
    checkboxLabel: 'I don’t have a website yet',
  },
  {
    title: "What's your company name?",
    type: 'doubleInput',
    fields: [
      { label: 'Company Name', placeholder: 'Company Name' },
      {
        label: "What's your business about?",
        placeholder:
          'Consider including basic details like name, industry, and what makes your business unique and valuable to your target audience.',
        textarea: true,
      },
    ],
  },
];

const answers = ref<Record<number, string>>({});

const currentStep = computed(() => steps[step.value - 1]);

function nextStep() {
  if (step.value < totalSteps) {
    step.value++;
  } else {
    // Завершение: можно отправить данные и закрыть
    open.value = false;
    // отправка answers.value на бэкенд и т.д.
  }
}

function prevStep() {
  if (step.value > 1) {
    step.value--;
  }
}

function closeModal() {
  open.value = false;
}
</script>
