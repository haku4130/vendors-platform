<template>
  <UCard
    class="h-full flex flex-col"
    :ui="{
      header: 'pt-0 px-0 sm:px-0',
      body: 'flex flex-col flex-1 overflow-scroll items-center',
    }"
  >
    <template #header>
      <UProgress
        :model-value="currentStep"
        :max="totalSteps"
        color="neutral"
        :ui="{ base: 'rounded-none' }"
      />
      <div class="flex justify-center text-muted mt-4">
        {{
          $t("vendorRegistration.step", {
            step: currentStep,
            total: totalSteps,
          })
        }}
      </div>
    </template>

    <UStepper
      ref="stepper"
      :items="items"
      :ui="{
        header: 'hidden',
        root: currentStep === 3 ? 'w-full my-auto' : 'w-fit my-auto',
        content: 'size-auto',
      }"
    >
      <template #main-goal>
        <h1 class="text-xl text-center font-bold mb-6">
          {{ $t("vendorRegistration.mainGoal.title") }}
        </h1>
        <UForm
          :ref="setFormRef('main-goal')"
          :state="answers"
          :schema="
            v.object({
              main_goal: v.pipe(
                v.string(),
                v.nonEmpty('This step is required'),
              ),
            })
          "
          class="space-y-4"
        >
          <UFormField name="main_goal" :ui="{ error: 'text-center' }">
            <URadioGroup
              v-model="answers.main_goal"
              variant="card"
              indicator="hidden"
              class="space-y-4"
              :items="mainGoalOptions"
            />
          </UFormField>
        </UForm>
      </template>

      <template #company-information>
        <h1 class="text-xl text-center font-bold mb-6">
          {{ $t("vendorRegistration.companyInfo.title") }}
        </h1>
        <UForm
          :ref="setFormRef('company-information')"
          :state="answers"
          :schema="
            v.object({
              description: v.pipe(
                v.string(),
                v.nonEmpty('This step is required'),
              ),
              company_website: v.pipe(
                v.string(),
                v.check(
                  (val) => val === '' || /^https?:\/\//.test(val),
                  'Invalid URL',
                ),
              ),
              min_project_size: v.pipe(
                v.number('Please input a number'),
                v.minValue(0, 'Should be positive'),
              ),
            })
          "
          class="space-y-4"
        >
          <UFormField
            :label="$t('vendorRegistration.companyInfo.description')"
            name="description"
          >
            <UTextarea
              v-model="answers.description"
              class="w-full"
              :rows="5"
              autoresize
              :placeholder="
                $t('vendorRegistration.companyInfo.descriptionPlaceholder')
              "
            />
          </UFormField>
          <UFormField
            :label="$t('vendorRegistration.companyInfo.website')"
            name="company_website"
          >
            <UInput
              v-model="answers.company_website"
              placeholder="https://yourcompany.com"
              class="w-full"
            />
          </UFormField>
          <UFormField
            :label="$t('vendorRegistration.companyInfo.minProject')"
            name="min_project_size"
          >
            <UInputNumber
              v-model="answers.min_project_size"
              class="w-full"
              :format-options="{
                style: 'currency',
                currency: 'USD',
              }"
            />
          </UFormField>
        </UForm>
      </template>

      <template #services>
        <h1 class="text-xl text-center font-bold mb-6">
          {{ $t("vendorRegistration.services.title") }}
        </h1>
        <UForm
          :ref="setFormRef('services')"
          :state="services"
          :schema="
            v.pipe(
              v.array(
                v.object({
                  id: v.string(),
                  label: v.string(),
                }),
              ),
              v.nonEmpty('This step is required'),
              v.maxLength(5, 'You can select up to 5 services'),
            )
          "
          class="space-y-4 max-w-xl mx-auto"
        >
          <UFormField :label="$t('vendorRegistration.services.title')">
            <ServiceTagsSelect
              v-model="services"
              :errors="forms['services']?.getErrors() || []"
            />
          </UFormField>
        </UForm>
      </template>
    </UStepper>

    <template #footer>
      <div class="flex gap-2 justify-between">
        <UButton
          leading-icon="i-lucide-chevron-left"
          class="hover:disabled:text-black"
          :disabled="!stepper?.hasPrev"
          @click="
            stepper?.prev();
            currentStep--;
          "
        >
          {{ $t("vendorRegistration.prev") }}
        </UButton>

        <UTooltip
          :delay-duration="0"
          :text="$t('vendorRegistration.completeStep')"
          :disabled="isValidCurrentStep"
          :disable-closing-trigger="true"
        >
          <UButton
            trailing-icon="i-lucide-chevron-right"
            variant="solid"
            :disabled="!isValidCurrentStep"
            @click="handleNextStep"
          >
            {{ $t("vendorRegistration.next") }}
          </UButton>
        </UTooltip>
      </div>
    </template>
  </UCard>
</template>

<script setup lang="ts">
import * as v from "valibot";
import type { StepperItem, Form } from "@nuxt/ui";
import type { VendorProfileCreate, ServicePublicShort } from "~/generated/api";
import { vendorsCreateVendorProfile } from "~/generated/api";

const { t } = useI18n();

const items: StepperItem[] = [
  { slot: "main-goal" as const },
  { slot: "company-information" as const },
  { slot: "services" as const },
];

const mainGoalOptions = computed(() => [
  t("vendorRegistration.mainGoal.option1"),
  t("vendorRegistration.mainGoal.option2"),
  t("vendorRegistration.mainGoal.option3"),
]);

const answers = ref<VendorProfileCreate>({
  main_goal: "",
  company_website: "",
  description: "",
  min_project_size: 100,
  service_ids: [],
});
const services = ref<ServicePublicShort[]>([]);

const totalSteps = items.length;
const currentStep = ref(1);

const stepper = useTemplateRef("stepper");

const forms = reactive<Record<string, Form<VendorProfileCreate> | null>>({});

function setFormRef(name: string) {
  return (el: Form<VendorProfileCreate> | null) => {
    forms[name] = el;
  };
}

async function handleNextStep() {
  const key = items[currentStep.value - 1]?.slot ?? "";

  const form = forms[key];
  if (!form) return;

  await form.submit();

  if (form.getErrors().length) {
    return;
  }

  if (currentStep.value === totalSteps) {
    return handleFinish();
  }
  stepper.value?.next();
  currentStep.value++;
}

const prepareAnswers = () => {
  return {
    ...answers.value,
    company_website: answers.value.company_website || null,
    service_ids: services.value.map((service) => service.id),
  };
};

const toast = useToast();

async function handleFinish() {
  const res = await vendorsCreateVendorProfile({
    body: prepareAnswers(),
  });
  if (!res.error) {
    toast.add({
      title: "Success",
      description: "Vendor Profile created successfully!",
      color: "success",
    });

    await useAuth().loadUser();
    navigateTo("/dashboard");
  } else {
    toast.add({
      title: "Vendor Profile creation failed",
      description: extractErrorMessage(res.error),
      color: "error",
    });
  }
}

const isValidCurrentStep = computed(() => {
  return !forms[items[currentStep.value - 1]?.slot ?? ""]?.getErrors().length;
});
</script>
