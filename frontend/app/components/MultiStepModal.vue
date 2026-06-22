<template>
  <UModal v-model:open="open" :title="title" :ui="modalUi" fullscreen>
    <UButton size="xl"> {{ triggerLabel }} </UButton>

    <template #body>
      <div class="flex flex-col w-full h-full">
        <UProgress
          v-if="phase === 'form'"
          :model-value="stepNumber"
          :max="totalSteps"
        />

        <div
          v-if="phase !== 'vendors'"
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
              <slot :name="'step-' + stepNumber"> </slot>
            </div>
          </template>

          <template v-else-if="phase === 'summary'">
            <ProjectSummary
              v-model="answers"
              @submit="$emit('finish-create')"
            />
          </template>
        </div>

        <div v-else-if="phase === 'vendors'" class="flex-1 overflow-y-auto">
          <div class="mx-auto max-w-5xl px-6 py-4">
            <VendorSelection :project-id="createdProjectId" />
          </div>
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
        {{ $t("multiStepModal.back") }}
      </UButton>
      <UTooltip
        :delay-duration="0"
        :text="$t('multiStepModal.completeStep')"
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
          {{ $t("multiStepModal.next") }}
        </UButton>
      </UTooltip>
    </template>
    <template v-else-if="phase === 'summary'" #footer>
      <div></div>
      <UButton variant="solid" size="xl" @click="$emit('finish-create')">
        {{ $t("multiStepModal.selectVendors") }}
      </UButton>
    </template>
    <template v-else-if="phase === 'vendors'" #footer>
      <div></div>
      <UButton variant="solid" size="xl" @click="finishAndClose">
        {{ $t("multiStepModal.sendToVendors") }}
      </UButton>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import type { AnswersType } from "@/types/answers";

const props = withDefaults(
  defineProps<{
    title?: string;
    triggerLabel?: string;
    stepIndex: number;
    totalSteps: number;
    isValidCurrentStep: boolean;
    createdProjectId: string;
    phase: "form" | "summary" | "vendors";
  }>(),
  {
    title: "Project Brief",
    triggerLabel: "Start a Project",
  },
);

const answers = defineModel<AnswersType>({ required: true });

const emit = defineEmits(["next-step", "prev-step", "finish-create", "finish"]);

const open = ref(false);
const stepNumber = computed(() => props.stepIndex + 1);

const modalUi = computed(() => {
  return {
    header: props.phase === "form" ? "bg-vendor-gradient" : "",
    footer: "justify-between",
    body: [
      props.phase === "form" ? "" : "bg-vendor-gradient",
      props.phase === "vendors" ? "!py-0" : "",
    ],
    title: props.phase === "form" ? "text-white" : "text-black",
    close: props.phase === "form" ? "text-white" : "text-black",
  };
});

function finishAndClose() {
  open.value = false;
  emit("finish");
}

defineExpose({ open });
</script>
