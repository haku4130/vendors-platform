<template>
  <div class="space-y-8">
    <section
      class="bg-vendor-gradient shadow-sm p-6 rounded-2xl flex flex-col lg:flex-row items-stretch gap-6"
    >
      <div class="lg:w-1/3 flex items-center">
        <h1 class="text-xl font-semibold text-gray-900 leading-snug">
          Find the perfect partner for your project
        </h1>
      </div>

      <div
        class="bg-white rounded-2xl flex flex-col lg:flex-row items-center justify-between gap-4 min-w-fit w-full lg:w-2/3 p-6"
      >
        <div class="flex flex-col gap-3 w-full">
          <UInput
            leading-icon="i-lucide-search"
            placeholder="Search web developers, SEO, UX..."
            :ui="{ base: 'rounded-full' }"
          />

          <UInput
            leading-icon="i-lucide-map-pin"
            placeholder="Any location"
            :ui="{ base: 'rounded-full' }"
          />
        </div>

        <div class="min-w-fit w-1/3 flex justify-center">
          <UButton size="xl" to="/dashboard/projects"> Find a Partner </UButton>
        </div>
      </div>
    </section>

    <section class="rounded-2xl p-6 shadow-sm space-y-4">
      <h3 class="text-lg font-semibold">My Projects</h3>
      <MyProjectGrid v-if="projects" :items="projects" class="my-6" />
      <div v-if="!projects" class="w-full">
        <h4 class="text-xl font-semibold">Build a project brief in minutes</h4>
        <p class="mt-1">
          Create a personalized project brief and send it to multiple best-fit
          vendors all at once.
        </p>
      </div>
      <MultiStepModal
        v-model="answers"
        :step-index="stepIndex"
        :total-steps="totalSteps"
        :is-valid-current-step="isValidCurrentStep"
        :phase="phase"
        title="Project Brief"
        @next-step="nextStep"
        @prev-step="stepIndex--"
        @finish-create="handleCreateFinish"
        @finish="handleFinish"
      >
        <template #step-1-title>
          Give your project a name as a short description.
        </template>
        <template #step-1>
          <UForm
            :ref="
              (el) => (formRefs[stepIndex] = el as unknown as Form<null> | null)
            "
            :state="answers"
            :schema="
              v.object({
                projectName: v.pipe(
                  v.string(),
                  v.nonEmpty('This step is required')
                ),
              })
            "
          >
            <UFormField
              name="projectName"
              help="What goal do you want to accomplish?"
            >
              <UTextarea
                v-model="answers.projectName"
                placeholder="E.g., Optimize website for faster performance / Grow website traffic through targeted keyword optimization / Make my website navigation more user friendly."
                size="xl"
                :rows="5"
                class="w-full"
                autoresize
              />
            </UFormField>
          </UForm>
        </template>

        <template #step-2-title>
          What kind of services are you looking for?
        </template>
        <template #step-2>
          <UForm
            :ref="
              (el) => (formRefs[stepIndex] = el as unknown as Form<null> | null)
            "
            :state="answers"
            :schema="
              v.object({
                servicesNeeded: v.pipe(
                  v.array(
                    v.object({
                      id: v.string(),
                      label: v.string(),
                    })
                  ),
                  v.nonEmpty('This step is required'),
                  v.maxLength(5, 'You can select up to 5 services')
                ),
              })
            "
          >
            <UFormField name="servicesNeeded">
              <ServiceTagsSelect
                v-model="answers.servicesNeeded"
                :errors="formRefs[stepIndex]?.getErrors() || []"
                placeholder="Search for Web Design, Web App Development, etc."
                @update:model-value="
                  formRefs[stepIndex]?.validate({ silent: true })
                "
              />
              <template #error><div /></template>
            </UFormField>
          </UForm>
        </template>

        <template #step-3-title>
          When would you like to start this project?
        </template>
        <template #step-3>
          <UForm
            :ref="
              (el) => (formRefs[stepIndex] = el as unknown as Form<null> | null)
            "
            :state="answers"
            :schema="
              v.object({
                startTime: v.pipe(
                  v.string(),
                  v.nonEmpty('This step is required')
                ),
              })
            "
          >
            <UFormField name="startTime" :ui="{ error: 'text-center' }">
              <URadioGroup
                v-model="answers.startTime"
                indicator="hidden"
                variant="card"
                orientation="horizontal"
                :items="['Within 30 days', 'Within 60 days', 'After 60+ days']"
                class="w-fit m-auto"
              />
            </UFormField>
          </UForm>
        </template>

        <template #step-4-title> What is your project budget? </template>
        <template #step-4>
          <UForm
            :ref="
              (el) => (formRefs[stepIndex] = el as unknown as Form<null> | null)
            "
            :state="answers"
            :schema="
              v.object({
                budget: v.number(),
              })
            "
          >
            <UFormField name="budget" :ui="{ error: 'text-center' }">
              <UInputNumber
                v-model="answers.budget"
                :format-options="{
                  style: 'currency',
                  currency: 'USD',
                }"
              />
            </UFormField>
          </UForm>
        </template>

        <template #step-5-title>
          What's important to you about a provider's location?
        </template>
        <template #step-5>
          <UForm
            :ref="
              (el) => (formRefs[stepIndex] = el as unknown as Form<null> | null)
            "
            :state="answers"
            :schema="
              v.object({
                locationPreference: v.pipe(
                  v.string(),
                  v.nonEmpty('This step is required')
                ),
              })
            "
          >
            <UFormField
              name="locationPreference"
              :ui="{ error: 'text-center' }"
            >
              <URadioGroup
                v-model="answers.locationPreference"
                indicator="hidden"
                variant="card"
                :items="[
                  {
                    label:
                      'No preference — just looking for the best providers',
                    value: 'no_preference',
                  },
                  {
                    label: 'Near me for in-person collaboration',
                    value: 'near_me',
                  },
                  {
                    label: 'I have specific location in mind',
                    value: 'specific',
                  },
                ]"
                class="w-full"
                :ui="{ fieldset: 'gap-y-2' }"
                @update:model-value="formRefs[stepIndex]?.clear()"
              />
              <UForm
                v-if="answers.locationPreference === 'specific'"
                :schema="
                  v.object({
                    exactLocation: v.pipe(
                      v.string(),
                      v.nonEmpty('This step is required')
                    ),
                  })
                "
                nested
              >
                <UFormField name="exactLocation">
                  <LocationSelector
                    v-if="answers.exactLocation !== null"
                    v-model="answers.exactLocation"
                    class="w-full mt-2"
                    @update:model-value="formRefs[stepIndex]?.clear()"
                  />
                </UFormField>
              </UForm>
            </UFormField>
          </UForm>
        </template>

        <template #step-6-title> What's your company's website? </template>
        <template #step-6>
          <UForm
            :ref="
              (el) => (formRefs[stepIndex] = el as unknown as Form<null> | null)
            "
            :state="answers"
            :schema="
              v.object({
                website: v.optional(v.string()),
              })
            "
          >
            <UFormField
              name="website"
              help="Optional"
              :ui="{ error: 'text-center' }"
            >
              <UInput
                v-model="answers.website"
                placeholder="https://yourcompany.com"
                size="xl"
                class="min-w-60"
              />
            </UFormField>
          </UForm>
        </template>

        <template #step-7-title>
          Tell us more about your project and goals.
        </template>
        <template #step-7>
          <UForm
            :ref="
              (el) => (formRefs[stepIndex] = el as unknown as Form<null> | null)
            "
            :state="answers"
            :schema="
              v.object({
                projectIntroduction: v.pipe(
                  v.string(),
                  v.nonEmpty('This step is required')
                ),
              })
            "
          >
            <UFormField name="projectIntroduction">
              <UTextarea
                v-model="answers.projectIntroduction"
                placeholder="Briefly describe your company, the challenges you’re facing, and what you aim to achieve with this project."
                size="xl"
                :rows="5"
                class="w-full"
                autoresize
              />
            </UFormField>
          </UForm>
        </template>
      </MultiStepModal>
    </section>

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
import * as v from 'valibot';
import type { AnswersType } from '@/types/answers';
import type { Form } from '@nuxt/ui';
import type { ProjectCreate, ProjectStart } from '~/generated/api';
import {
  projectsCreateNewProject,
  projectsListMyProjects,
} from '~/generated/api';

const auth = useAuth();

const { data: projects } = await projectsListMyProjects();

const stepIndex = ref(0);
const totalSteps = ref(7);

const formRefs = reactive<Record<number, Form<null> | null>>({});

async function nextStep() {
  if (
    await formRefs[stepIndex.value]?.validate({ silent: true, nested: true })
  ) {
    if (stepIndex.value < totalSteps.value - 1) stepIndex.value++;
    else {
      determineLocation(answers);
      phase.value = 'summary';
    }
  }
}

function determineLocation(answers: AnswersType): string | null {
  if (answers.locationPreference === 'no_preference') {
    answers.exactLocation = null;
  } else if (answers.locationPreference === 'near_me') {
    answers.exactLocation = auth.user.value?.location || null;
  }
  return answers.exactLocation;
}

const isValidCurrentStep = computed(() => {
  return !formRefs[stepIndex.value]?.getErrors().length;
});

const phase = ref<'form' | 'summary' | 'vendors'>('form');

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

function transformAnswersToProject(answers: AnswersType): ProjectCreate {
  return {
    title: answers.projectName,
    description: answers.projectIntroduction,
    start_date: answers.startTime as ProjectStart,
    location: determineLocation(answers),
    website: answers.website || null,
    service_ids: answers.servicesNeeded.map((s) => s.id),
    budget: answers.budget,
    questions: answers.questions.length > 0 ? answers.questions : null,
    requirements: answers.requirements.length > 0 ? answers.requirements : null,
  };
}

const toast = useToast();

async function handleCreateFinish() {
  const res = await projectsCreateNewProject({
    body: transformAnswersToProject(answers),
  });
  if (!res.error) {
    toast.add({
      title: 'Success',
      description: 'Project created successfully!',
      color: 'success',
    });

    phase.value = 'vendors';
  } else {
    let detail: string;

    if (typeof res.error.detail === 'string') {
      detail = res.error.detail;
    } else if (Array.isArray(res.error.detail)) {
      detail = res.error.detail[0]?.msg ?? 'Something went wrong';
    } else {
      detail = 'Something went wrong';
    }

    toast.add({
      title: 'Project creation failed',
      description: detail,
      color: 'error',
    });
  }
}

function handleFinish() {
  console.log('📦 Итоговые ответы:', answers);
}

const answers = reactive<AnswersType>({
  projectName: '',
  servicesNeeded: [],
  startTime: '',
  budget: 150,
  locationPreference: '',
  exactLocation: '',
  website: '',
  projectIntroduction: '',
  questions: [],
  requirements: [],
});
</script>
