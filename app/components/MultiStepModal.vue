<template>
  <UModal
    v-model:open="open"
    :title="title"
    :ui="{
      header: phase === 'form' ? 'bg-[#F7A86B]' : '',
      footer: 'justify-between',
      body: phase === 'form' ? '' : 'bg-[#F7A86B]',
    }"
    fullscreen
  >
    <!-- Кнопка открытия -->
    <button
      class="border border-black rounded-md px-4 py-2 font-medium hover:bg-black hover:text-white transition"
    >
      {{ triggerLabel }}
    </button>

    <!-- Основной контент -->
    <template #body>
      <div class="flex flex-col w-full h-full">
        <!-- Прогресс -->
        <UProgress
          v-if="phase === 'form'"
          v-model="step"
          :max="totalSteps"
          color="neutral"
        />

        <div
          class="flex-1 flex flex-col items-center justify-center px-8 text-center"
        >
          <!-- Форма (1–6 шаги) -->
          <template v-if="phase === 'form'">
            <p class="text-sm text-gray-700 mb-1">
              Step {{ step }} / {{ totalSteps }}
            </p>
            <h3 class="text-xl font-semibold text-gray-900 mb-6">
              {{ currentStep.title }}
            </h3>

            <slot
              name="step"
              :step="currentStep"
              :answers="answers"
              :step-index="step"
            />
          </template>

          <!-- Сводка проекта -->
          <template v-else-if="phase === 'summary'">
            <ProjectSummary
              :data="answers"
              @edit="handleEdit"
              @submit="goToVendors"
            />
          </template>

          <!-- Выбор вендоров -->
          <template v-else-if="phase === 'vendors'">
            <VendorSelection :project-data="answers" @send="finishAndClose" />
          </template>
        </div>
      </div>
    </template>

    <!-- Навигация -->
    <template v-if="phase === 'form'" #footer>
      <button
        class="px-4 py-2 border border-gray-800 rounded-md transition hover:bg-gray-800 hover:text-white disabled:opacity-50 disabled:pointer-events-none disabled:hover:bg-transparent disabled:hover:text-gray-800"
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
    <template v-else-if="phase === 'summary'" #footer>
      <div />
      <button
        class="px-6 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition"
        @click="goToVendors"
      >
        Select Vendors
      </button>
    </template>
    <template v-else-if="phase === 'vendors'" #footer>
      <div />
      <button
        class="px-6 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-700 transition"
        @click="goToVendors"
      >
        Send to Vendors
      </button>
    </template>
  </UModal>
</template>

<script setup lang="ts">
const props = defineProps({
  title: { type: String, default: 'Project Brief' },
  triggerLabel: { type: String, default: 'Start a Project' },
  steps: { type: Array, required: true },
});

const emit = defineEmits(['finish']);

const open = ref(false);
const step = ref(1);
const totalSteps = computed(() => props.steps.length);
const answers = ref<Record<number, any>>({});
const phase = ref<'form' | 'summary' | 'vendors'>('form');

const currentStep = computed(() => props.steps[step.value - 1]);

function nextStep() {
  if (step.value < totalSteps.value) step.value++;
  else {
    phase.value = 'summary';
  }
}
function prevStep() {
  if (step.value > 1) step.value--;
}
function handleEdit() {
  phase.value = 'form';
}
function goToVendors() {
  phase.value = 'vendors';
}
function finishAndClose() {
  open.value = false;
}
</script>
