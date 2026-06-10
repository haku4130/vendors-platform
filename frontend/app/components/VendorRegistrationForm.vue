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
        root: currentStep === 5 ? 'w-full my-auto' : 'w-fit my-auto',
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
              sales_email: v.pipe(
                v.string(),
                v.email('Invalid email'),
                v.nonEmpty('Sales Email is required'),
              ),
              admin_contact_phone: v.pipe(
                v.string(),
                v.nonEmpty('Phone number is required'),
              ),
              employee_count: v.pipe(
                v.number('Please input a number'),
                v.minValue(1, 'Employee count should be greater than 1'),
              ),
              company_website: v.pipe(
                v.string(),
                v.url('Invalid URL'),
                v.nonEmpty('Company website is required'),
              ),
              founded_year: v.pipe(
                v.number('Please input a number'),
                v.minValue(1900, 'Enter valid founding year'),
                v.maxValue(
                  new Date().getFullYear(),
                  'Enter valid founding year',
                ),
              ),
              turnover: v.pipe(
                v.number('Please input a number'),
                v.minValue(0, 'Turnover should be positive'),
              ),
            })
          "
          class="space-y-4"
        >
          <UFormField
            :label="$t('vendorRegistration.companyInfo.salesEmail')"
            name="sales_email"
          >
            <UInput
              v-model="answers.sales_email"
              placeholder="example@mail.com"
              icon="i-lucide-at-sign"
              class="w-full"
            />
          </UFormField>
          <UFormField
            :label="$t('vendorRegistration.companyInfo.phone')"
            name="admin_contact_phone"
          >
            <UFieldGroup class="w-full">
              <USelectMenu
                v-model="phone_country_code"
                placeholder="Code"
                label-key="dial_code"
                :loading="status === 'pending'"
                :items="country_codes"
                :filter-fields="['dial_code', 'code', 'name']"
                :ui="{
                  content: 'min-w-fit',
                  trailingIcon: 'hidden',
                  base: 'pe-2',
                }"
                @update:open="onOpen"
              >
                <template #leading="{ modelValue, ui }">
                  <span v-if="modelValue" class="size-5 text-center">
                    {{ modelValue?.emoji }}
                  </span>
                  <UIcon
                    v-else
                    name="i-lucide-phone"
                    :class="ui.leadingIcon()"
                  />
                </template>
                <template #item-leading="{ item }">
                  <span class="size-5 text-center">
                    {{ item.emoji }}
                  </span>
                </template>
                <template #item-label="{ item }">
                  {{ item.dial_code }} · {{ item.code }}
                </template>
              </USelectMenu>
              <UInput v-model="contact_phone" type="tel" class="w-full" />
            </UFieldGroup>
          </UFormField>
          <UFormField
            :label="$t('vendorRegistration.companyInfo.employees')"
            name="employee_count"
          >
            <UInputNumber v-model="answers.employee_count" class="w-full" />
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
            :label="$t('vendorRegistration.companyInfo.foundingYear')"
            name="founded_year"
          >
            <UInputNumber
              v-model="answers.founded_year"
              class="w-full"
              :format-options="{
                useGrouping: false,
                maximumFractionDigits: 0,
              }"
            />
          </UFormField>
          <UFormField
            :label="$t('vendorRegistration.companyInfo.turnover')"
            name="turnover"
          >
            <UInputNumber
              v-model="answers.turnover"
              class="w-full"
              :format-options="{
                style: 'currency',
                currency: 'USD',
              }"
            />
          </UFormField>
        </UForm>
      </template>

      <template #description-step>
        <h1 class="text-xl text-center font-bold mb-6">
          {{ $t("vendorRegistration.description.title") }}
        </h1>
        <UForm
          :ref="setFormRef('description-step')"
          :state="answers"
          :schema="
            v.object({
              description: v.pipe(
                v.string(),
                v.nonEmpty('This step is required'),
              ),
            })
          "
          class="space-y-4"
        >
          <UFormField name="description">
            <UTextarea
              v-model="answers.description"
              class="w-full"
              :rows="5"
              autoresize
              placeholder="Describe your company, its mission, and values."
            />
          </UFormField>
        </UForm>
      </template>

      <template #project-size>
        <h1 class="text-xl text-center font-bold mb-6">
          {{ $t("vendorRegistration.projectSize.title") }}
        </h1>
        <UForm
          :ref="setFormRef('project-size')"
          :state="answers"
          :schema="
            v.object({
              min_project_size: v.pipe(
                v.number('Please input a number'),
                v.minValue(0, 'Should be positive'),
              ),
              avg_hourly_rate: v.pipe(
                v.number('Please input a number'),
                v.minValue(0, 'Should be positive'),
              ),
            })
          "
          class="space-y-4"
        >
          <UFormField
            :label="$t('vendorRegistration.projectSize.minProject')"
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
          <UFormField
            :label="$t('vendorRegistration.projectSize.hourlyRate')"
            name="avg_hourly_rate"
          >
            <UInputNumber
              v-model="answers.avg_hourly_rate"
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
          <UFormField :label="$t('vendorRegistration.projectSize.minProject')">
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
  { slot: "description-step" as const },
  { slot: "project-size" as const },
  { slot: "services" as const },
];

const mainGoalOptions = computed(() => [
  t("vendorRegistration.mainGoal.option1"),
  t("vendorRegistration.mainGoal.option2"),
  t("vendorRegistration.mainGoal.option3"),
]);

const answers = ref<VendorProfileCreate>({
  main_goal: "",
  sales_email: "",
  admin_contact_phone: "",
  employee_count: 15,
  company_website: "",
  founded_year: 2000,
  turnover: 15000,
  description: "",
  min_project_size: 100,
  avg_hourly_rate: 15,
  service_ids: [],
});
const services = ref<ServicePublicShort[]>([]);
const phone_country_code = ref();
const contact_phone = ref();

const fullPhoneNumber = computed({
  get: () => {
    if (phone_country_code.value?.dial_code && contact_phone.value) {
      return `${phone_country_code.value.dial_code}${contact_phone.value}`;
    }
    return "";
  },
  set: (value: string) => {
    answers.value.admin_contact_phone = value;
  },
});

watch(fullPhoneNumber, (newValue) => {
  answers.value.admin_contact_phone = newValue;
});

const {
  data: country_codes,
  status,
  execute,
} = await useLazyFetch<
  {
    name: string;
    code: string;
    emoji: string;
    unicode: string;
    image: string;
    dial_code: string;
  }[]
>("/countries.json", {
  immediate: false,
});

function onOpen() {
  if (!country_codes.value?.length) {
    execute();
  }
}

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
