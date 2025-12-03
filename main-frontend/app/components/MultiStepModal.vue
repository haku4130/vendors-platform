<template>
  <UModal
    v-model:open="open"
    :title="title"
    :ui="{
      header: phase === 'form' ? 'bg-vendor-gradient' : '',
      footer: 'justify-between',
      body: phase === 'form' ? '' : 'bg-vendor-gradient',
    }"
    fullscreen
  >
    <UButton size="xl"> {{ triggerLabel }} </UButton>

    <template #body>
      <div class="flex flex-col w-full h-full">
        <UProgress
          v-if="phase === 'form'"
          :model-value="stepNumber"
          :max="totalSteps"
          color="neutral"
        />

        <div
          class="flex-1 flex flex-col items-center justify-center my-4 text-center"
        >
          <template v-if="phase === 'form'">
            <p class="text-sm text-gray-700 mb-1">
              Step {{ stepNumber }} / {{ totalSteps }}
            </p>
            <h3 class="text-xl font-semibold text-gray-900 my-3">
              <slot :name="'step-' + stepNumber + '-title'">
                Step {{ stepNumber }}
              </slot>
            </h3>

            <div class="w-full max-w-xl">
              <slot :name="'step-' + stepNumber" />
            </div>
          </template>

          <template v-else-if="phase === 'summary'">
            <ProjectSummary
              v-model="answers"
              @submit="$emit('finish-create')"
            />
          </template>

          <template v-else-if="phase === 'vendors'">
            <VendorSelection :project-id="createdProjectId" />
          </template>
        </div>
      </div>
    </template>

    <template v-if="phase === 'form'" #footer>
      <UButton
        size="xl"
        :disabled="stepIndex === 0"
        class="hover:disabled:text-black"
        leading-icon="i-lucide-chevron-left"
        @click="$emit('prev-step')"
      >
        Back
      </UButton>
      <UTooltip
        :delay-duration="0"
        text="Please complete the current step before proceeding"
        :disabled="isValidCurrentStep"
        :disable-closing-trigger="true"
      >
        <UButton
          variant="solid"
          trailing-icon="i-lucide-chevron-right"
          size="xl"
          :disabled="!isValidCurrentStep"
          @click="$emit('next-step')"
        >
          Next
        </UButton>
      </UTooltip>
    </template>
    <template v-else-if="phase === 'summary'" #footer>
      <div />
      <UButton variant="solid" size="xl" @click="$emit('finish-create')">
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
import type { AnswersType } from '@/types/answers';

const {
  title = 'Project Brief',
  triggerLabel = 'Start a Project',
  stepIndex,
} = defineProps<{
  title?: string;
  triggerLabel?: string;
  stepIndex: number;
  totalSteps: number;
  isValidCurrentStep: boolean;
  createdProjectId: string;
  phase: 'form' | 'summary' | 'vendors';
}>();

const answers = defineModel<AnswersType>({ required: true });

defineEmits(['next-step', 'prev-step', 'finish-create']);

const open = ref(false);
const stepNumber = computed(() => stepIndex + 1);

function finishAndClose() {
  open.value = false;
}
</script>
