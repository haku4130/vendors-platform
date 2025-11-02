<template>
  <div class="space-y-8">
    <!-- Top Search Block -->
    <section
      class="bg-[#F7A86B] shadow-sm p-6 rounded-2xl flex flex-col lg:flex-row items-stretch gap-6"
    >
      <!-- Левая часть -->
      <div class="lg:w-1/3 flex items-center">
        <h2 class="text-xl font-semibold text-gray-900 leading-snug">
          Find the perfect partner for your project
        </h2>
      </div>

      <!-- Правая часть -->
      <div
        class="bg-white rounded-2xl flex flex-col lg:flex-row items-center justify-between gap-4 min-w-fit w-full lg:w-2/3 p-6"
      >
        <div class="flex flex-col gap-3 w-full">
          <div
            class="flex items-center border border-black rounded-full px-4 py-2 flex-1"
          >
            <UIcon name="mdi:magnify" size="20" class="text-gray-600 mr-2" />
            <input
              type="text"
              placeholder="Search web developers, SEO, UX..."
              class="flex-1 bg-transparent outline-none placeholder:text-gray-500 text-gray-800"
            />
          </div>

          <div
            class="flex items-center border border-black rounded-full px-4 py-2 flex-1"
          >
            <UIcon
              name="mdi:map-marker-outline"
              size="20"
              class="text-gray-600 mr-2"
            />
            <input
              type="text"
              placeholder="Any location"
              class="flex-1 bg-transparent outline-none placeholder:text-gray-500 text-gray-800"
            />
          </div>
        </div>

        <div class="min-w-fit w-1/3 flex justify-center">
          <UButton size="xl"> Find a Vendor </UButton>
        </div>
      </div>
    </section>

    <!-- My Projects -->
    <section class="bg-white rounded-2xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold mb-4">My Projects</h3>
      <div class="flex flex-col md:flex-row gap-6">
        <UIcon name="icon-park-outline:list" size="50" class="text-gray-700" />
        <div>
          <div class="mb-4">
            <h4 class="text-xl font-semibold">
              Build a project brief in minutes
            </h4>
            <p class="text-gray-700 mt-1">
              Create a personalized project brief and send it to multiple
              best-fit vendors all at once.
            </p>
          </div>
          <MultiStepModal
            v-model:answers="answers"
            :steps="steps"
            :form-refs="formRefs"
            title="Project Brief"
            @finish="handleFinish"
          >
            <template #step-1="{ step, stepIndex }">
              <UForm
                :ref="(el) => setFormRef(stepIndex, el)"
                :validate="() => validate(stepIndex)"
              >
                <UFormField :name="step?.key">
                  <UTextarea
                    v-model="answers[step?.key] as string"
                    :placeholder="step?.placeholder"
                    size="xl"
                    :rows="5"
                    class="w-full"
                    autoresize
                  />
                </UFormField>
              </UForm>
            </template>

            <template #step-2="{ step, stepIndex }">
              <UForm
                :ref="(el) => setFormRef(stepIndex, el)"
                :validate="() => validate(stepIndex)"
              >
                <UFormField :name="step?.key">
                  <UInput
                    v-model="answers[step?.key]"
                    :placeholder="step?.placeholder"
                    size="xl"
                    class="w-full"
                  />
                </UFormField>
              </UForm>
            </template>

            <template #step-3="{ step, stepIndex }">
              <UForm
                :ref="(el) => setFormRef(stepIndex, el)"
                :validate="() => validate(stepIndex)"
              >
                <UFormField :name="step?.key">
                  <URadioGroup
                    v-model="answers[step?.key] as string"
                    indicator="hidden"
                    variant="card"
                    orientation="horizontal"
                    :items="step?.options"
                    class="w-fit m-auto"
                  />
                </UFormField>
              </UForm>
            </template>

            <template #step-4="{ step, stepIndex }">
              <UForm
                :ref="(el) => setFormRef(stepIndex, el)"
                :validate="() => validate(stepIndex)"
              >
                <UFormField :name="step?.key">
                  <URadioGroup
                    v-model="answers[step?.key] as string"
                    indicator="hidden"
                    variant="card"
                    :items="step?.options"
                    class="w-fit m-auto"
                  />
                </UFormField>
              </UForm>
            </template>

            <template #step-5="{ step, stepIndex }">
              <UForm
                :ref="(el) => setFormRef(stepIndex, el)"
                :validate="() => validate(stepIndex)"
              >
                <UFormField :name="step?.key">
                  <UInput
                    v-model="answers[step?.key]"
                    :placeholder="step?.placeholder"
                    :disabled="answers['noWebsite']"
                    size="xl"
                  />
                </UFormField>
                <UFormField>
                  <UCheckbox
                    v-model="answers['noWebsite']"
                    :label="step?.checkboxLabel"
                    class="w-fit m-auto mt-3"
                  />
                </UFormField>
              </UForm>
            </template>

            <template #step-6="{ step, stepIndex }">
              <UForm
                :ref="(el) => setFormRef(stepIndex, el)"
                :validate="() => validate(stepIndex)"
              >
                <UFormField :name="step?.key + '.companyName'">
                  <UInput
                    v-model="answers[step?.key]['companyName']"
                    :placeholder="step?.fields?.['companyName']?.placeholder"
                    size="xl"
                    class="w-full"
                  />
                </UFormField>
                <UFormField :name="step?.key + '.companyAbout'">
                  <h3 class="text-xl font-semibold text-gray-900 mt-10 mb-3">
                    {{ step?.fields?.['companyAbout']?.label }}
                  </h3>
                  <UTextarea
                    v-model="answers[step?.key]['companyAbout']"
                    :placeholder="step?.fields?.['companyAbout']?.placeholder"
                    size="xl"
                    :rows="4"
                    class="w-full"
                    autoresize
                  />
                </UFormField>
              </UForm>
            </template>
          </MultiStepModal>
        </div>
      </div>
    </section>

    <!-- My Recommendations -->
    <section class="bg-white rounded-2xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold mb-4">My Recommendations</h3>
      <div class="grid lg:grid-cols-2 xl:grid-cols-3 gap-3">
        <div
          v-for="review in displayedReviews"
          :key="review.id"
          class="border border-gray-300 rounded-lg p-3 bg-gray-50"
        >
          <div class="flex items-center justify-between mb-1">
            <span class="font-semibold text-sm text-gray-900">{{
              review.commentedCompany
            }}</span>
            <div class="flex items-center gap-0.5 text-yellow-500 text-xs">
              <StarRating :rating="review.rating" />
            </div>
          </div>
          <p class="text-sm text-gray-700 leading-snug line-clamp-3">
            {{ review.text }}
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { Step } from '@/types/step';
import type { AnswersType } from '@/types/answers';
import type { FormError } from '@nuxt/ui';

interface FormRef {
  validate: () => Promise<boolean>;
}

const formRefs = reactive<Record<number, FormRef | null>>({});

const setFormRef = (stepIndex: number, el: unknown) => {
  if (el && typeof el === 'object' && 'validate' in el) {
    formRefs[stepIndex] = el as FormRef;
  } else {
    formRefs[stepIndex] = null;
  }
};

const validate = (stepIndex: number): FormError[] => {
  const step = steps[stepIndex];
  const errors: FormError[] = [];

  if (!step) return errors;

  const stepKey = step.key;
  const stepAnswers = answers[stepKey];

  // Если шаг — обычное текстовое поле
  if (typeof stepAnswers === 'string' && !step.checkboxLabel) {
    if (!stepAnswers.trim()) {
      errors.push({
        name: stepKey,
        message: 'This field is required',
      });
    }
  }

  // Если шаг — с checkbox
  else if (step.checkboxLabel) {
    const value = answers[stepKey];
    const noWebsite = answers['noWebsite'];
    if (!value && !noWebsite) {
      errors.push({
        name: stepKey,
        message: 'Either input a website or select [no website] option',
      });
    }
  }

  // Если у шага есть fields (как в companyInfo)
  else if (step.fields && typeof stepAnswers === 'object') {
    for (const [fieldKey, field] of Object.entries(step.fields)) {
      const value = stepAnswers[fieldKey];
      if (!value || (typeof value === 'string' && value.trim() === '')) {
        errors.push({
          name: `${stepKey}.${fieldKey}`,
          message: 'This field is required',
        });
      }
    }
  }

  return errors;
};

const myReviews = [
  {
    id: 1,
    commentedCompany: 'Acme Corp',
    rating: 5,
    text: 'They delivered our project ahead of time and exceeded expectations.',
  },
  {
    id: 2,
    commentedCompany: 'Beta LLC',
    rating: 4,
    text: 'Very professional team, great communication throughout the process.',
  },
  {
    id: 3,
    commentedCompany: 'Gamma Inc',
    rating: 5,
    text: 'Excellent work on our UI/UX design — creative and detail-oriented.',
  },
];

const displayedReviews = computed(() => myReviews?.slice(0, 3) || []);

function handleFinish(data: Record<string, unknown>) {
  console.log('📦 Итоговые ответы:', data);
}

// пример: отправка на сервер
// function sendToServer(data: Record<string, unknown>) {
//   fetch('/api/brief', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data),
//   })
//     .then((r) => r.json())
//     .then((res) => {
//       console.log('✅ Успешно отправлено:', res);
//     })
//     .catch((err) => console.error('❌ Ошибка при отправке:', err));
// }

const steps: Step[] = [
  {
    key: 'projectDescription',
    title: "What's your project about? What goals do you want to accomplish?",
    placeholder:
      'E.g., Optimize website for faster performance / Grow website traffic through targeted keyword optimization / Make my website navigation more user friendly.',
  },
  {
    key: 'companyType',
    title: 'What kind of company are you looking for?',
    placeholder: 'Search for SEO, web development, etc.',
  },
  {
    key: 'startTime',
    title: 'When would you like to start this project?',
    options: ['Within 30 days', 'Within 60 days', 'After 60+ days'],
  },
  {
    key: 'locationPreference',
    title: "What's important to you about a provider's location?",
    options: [
      'No preference — just looking for the best providers',
      'Near me for in-person collaboration',
      'I have specific countries in mind',
    ],
    optionsColumns: true,
  },
  {
    key: 'website',
    title: "What's your company's website?",
    placeholder: 'www.yourcompany.com',
    checkboxLabel: 'I don’t have a website yet',
  },
  {
    key: 'companyInfo',
    title: "What's your company name?",
    fields: {
      companyName: { placeholder: 'Company Name' },
      companyAbout: {
        label: "What's your business about?",
        placeholder:
          'Consider including basic details like name, industry, and what makes your business unique and valuable to your target audience.',
      },
    },
  },
];

const answers = reactive<AnswersType>({
  projectDescription: '',
  companyType: '',
  startTime: '',
  locationPreference: '',
  website: '',
  noWebsite: false,
  companyInfo: {
    companyName: '',
    companyAbout: '',
  },
});

watch(
  () => answers['noWebsite'],
  (checked) => {
    if (checked) {
      answers['website'] = '';
      const form = formRefs[4]; // или formRefs[stepIndex], если знаешь индекс текущего шага
      form?.setErrors([]); // очищает все ошибки
    }
  }
);
</script>
