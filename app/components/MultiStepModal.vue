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
    <UButton size="xl"> {{ triggerLabel }} </UButton>

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
      <UButton
        size="xl"
        :disabled="step === 1"
        class="hover:disabled:text-black"
        @click="prevStep"
      >
        Back
      </UButton>
      <UButton variant="solid" size="xl" @click="nextStep">
        {{ step === totalSteps ? 'Finish' : 'Next' }}
      </UButton>
    </template>
    <template v-else-if="phase === 'summary'" #footer>
      <div />
      <UButton variant="solid" size="xl" @click="goToVendors">
        Select Vendors
      </UButton>
    </template>
    <template v-else-if="phase === 'vendors'" #footer>
      <div />
      <UButton variant="solid" size="xl" @click="finishAndClose">
        Send to Vendors
      </UButton>
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
