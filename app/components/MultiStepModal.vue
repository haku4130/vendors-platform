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
          v-model="stepNumber"
          :max="totalSteps"
          color="neutral"
        />

        <div
          class="flex-1 flex flex-col items-center justify-center px-8 my-4 text-center"
        >
          <!-- Форма -->
          <template v-if="phase === 'form'">
            <p class="text-sm text-gray-700 mb-1">
              Step {{ stepNumber }} / {{ totalSteps }}
            </p>
            <h3 class="text-xl font-semibold text-gray-900 my-3">
              {{ currentStep?.title }}
            </h3>

            <div class="w-full max-w-xl">
              <slot
                :name="'step-' + stepNumber"
                :step="currentStep"
                :step-index="stepIndex"
              />
            </div>
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
        :disabled="stepIndex === 0"
        class="hover:disabled:text-black"
        leading-icon="material-symbols:chevron-left-rounded"
        @click="prevStep"
      >
        Back
      </UButton>
      <UTooltip
        :delay-duration="0"
        :text="
          isValidCurrentStep
            ? ''
            : 'Please complete the current step before proceeding'
        "
      >
        <UButton
          variant="solid"
          trailing-icon="material-symbols:chevron-right-rounded"
          size="xl"
          :disabled="!isValidCurrentStep"
          @click="nextStep"
        >
          Next
        </UButton>
      </UTooltip>
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
import type { Step } from '@/types/step';
import type { AnswersType } from '@/types/answers';

interface FormRef {
  validate: () => Promise<boolean>;
}

interface Props {
  title?: string;
  triggerLabel?: string;
  steps: Step[];
  formRefs: Record<number, FormRef | null>;
}

const {
  title = 'Project Brief',
  triggerLabel = 'Start a Project',
  steps,
  formRefs,
} = defineProps<Props>();

const answers = defineModel<AnswersType>();

const emit = defineEmits(['finish']);

const open = ref(false);
const stepIndex = ref(0);
const stepNumber = computed(() => stepIndex.value + 1);
const totalSteps = computed(() => steps.length);

const phase = ref<'form' | 'summary' | 'vendors'>('form');

const currentStep = computed<Step>(() => steps[stepIndex.value]);

const isValidCurrentStep = computed(() => {
  const currentForm = formRefs[stepIndex.value];
  if (!currentForm) return currentStep.value.required ? false : true;
  const errors = currentForm.getErrors?.();
  return !errors || errors.length === 0;
});

async function nextStep() {
  const currentForm = formRefs[stepIndex.value];
  if (currentForm) {
    try {
      await currentForm.validate();
    } catch {
      // если выброшено исключение — валидация не пройдена
      return;
    }
  }

  if (stepNumber.value < totalSteps.value) stepIndex.value++;
  else phase.value = 'summary';
}

function prevStep() {
  if (stepIndex.value > 0) stepIndex.value--;
}
function handleEdit() {
  phase.value = 'form';
}
function goToVendors() {
  phase.value = 'vendors';
  emit('finish');
}
function finishAndClose() {
  open.value = false;
}
</script>
