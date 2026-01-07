<template>
  <UContainer class="py-6">
    <h1 class="text-2xl font-semibold mb-6">
      Request for {{ data.projectName }} Services
    </h1>
    <section id="key-information" class="mb-8">
      <SectionHeader
        title="Key Information"
        :editable="fromAuthor"
        edit-inline
        @edit="editKeyInformation = true"
        @finish-edit="editKeyInformation = false"
      />
      <div
        class="border border-gray-400 rounded-lg overflow-hidden divide-y divide-gray-400 text-sm"
      >
        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-building" class="text-xl text-muted" />
            <span class="font-bold"> Company Name </span>
          </div>
          <span class="flex items-center">{{ companyName }}</span>
        </div>

        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-briefcase" class="text-xl text-muted" />
            <span class="font-bold"> Project Name </span>
          </div>
          <UInput
            v-if="editKeyInformation"
            v-model="data.projectName"
            class="w-5/12"
          />
          <span v-else class="flex items-center">{{ data.projectName }}</span>
        </div>

        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-calendar" class="text-xl text-muted" />
            <span class="font-bold"> Project Start Date </span>
          </div>
          <USelect
            v-if="editKeyInformation"
            v-model="data.startTime"
            :items="['Within 30 days', 'Within 60 days', 'After 60+ days']"
            :ui="{ trailingIcon: 'text-normal' }"
          />
          <span v-else class="flex items-center">{{ data.startTime }}</span>
        </div>

        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-dollar-sign" class="text-xl text-muted" />
            <span class="font-bold"> Project Budget </span>
          </div>
          <UInputNumber
            v-if="editKeyInformation"
            v-model="data.budget"
            :format-options="{
              style: 'currency',
              currency: 'USD',
            }"
          />
          <span v-else class="flex items-center">${{ data.budget }}</span>
        </div>

        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-map-pin" class="text-xl text-muted" />
            <span class="font-bold"> Location </span>
          </div>

          <span v-if="data.exactLocation === null" class="flex items-center"
            >No preference</span
          >
          <LocationSelector
            v-else-if="editKeyInformation"
            v-model="data.exactLocation"
            :icon="null"
            class="w-1/3"
          />
          <span v-else class="flex items-center">{{ data.exactLocation }}</span>
        </div>

        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-user" class="text-xl text-muted" />
            <span class="font-bold"> Contact Person </span>
          </div>
          <div class="text-right flex flex-col items-end">
            <span>{{ contactName }}</span>
            <span class="font-semibold">{{ contactEmail }}</span>
          </div>
        </div>

        <div
          v-if="data.website"
          class="flex justify-between px-4 py-3 min-h-16"
        >
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-globe" class="text-xl text-muted" />
            <span class="font-bold"> Company Website </span>
          </div>
          <UInput v-if="editKeyInformation" v-model="data.website" />
          <span v-else class="flex items-center">{{ data.website }}</span>
        </div>
      </div>
    </section>

    <section id="introduction" class="mb-8">
      <SectionHeader
        title="Introduction"
        :editable="fromAuthor"
        edit-inline
        @edit="editIntroduction = true"
        @finish-edit="editIntroduction = false"
      />
      <UTextarea
        v-if="editIntroduction"
        v-model="data.projectIntroduction"
        class="w-full"
        :rows="6"
      />
      <p v-else>
        {{ data.projectIntroduction }}
      </p>
    </section>

    <section id="services" class="mb-8">
      <SectionHeader
        title="Services Needed"
        :editable="fromAuthor"
        edit-inline
        @edit="editServices = true"
        @finish-edit="editServices = false"
      />
      <div class="border border-gray-300 rounded-md p-3 min-h-14">
        <ServiceTagsSelect
          v-if="editServices"
          v-model="data.servicesNeeded"
          :errors="[]"
          placeholder="Search for Web Design, Web App Development, etc."
        />
        <div v-else class="flex flex-wrap gap-2">
          <div
            v-for="(tag, i) in data.servicesNeeded"
            :key="i"
            class="px-3 py-1.5 rounded-sm inline-flex items-center gap-1.5 ring ring-inset ring-accented bg-elevated text-default data-disabled:cursor-not-allowed data-disabled:opacity-75 text-xs"
          >
            <span class="truncate">
              {{ tag.label }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <section id="questions" class="mb-8">
      <SectionHeader
        title="Questions"
        :editable="fromAuthor"
        edit-inline
        @edit="editQuestions = true"
        @finish-edit="editQuestions = false"
      />
      <ListInput
        v-model="data.questions"
        :editing="editQuestions"
        add-item-placeholder="Add a question"
        :no-items-text="
          fromAuthor
            ? 'You can add your questions to vendors here.'
            : 'The author has not added any questions.'
        "
      />
    </section>

    <section id="requirements">
      <SectionHeader
        title="Requirements"
        :editable="fromAuthor"
        edit-inline
        @edit="editRequirements = true"
        @finish-edit="editRequirements = false"
      />
      <ListInput
        v-model="data.requirements"
        :editing="editRequirements"
        add-item-placeholder="Add a requirement"
        :no-items-text="
          fromAuthor
            ? 'You can add your project requirements here.'
            : 'The author has not added any requirements.'
        "
      />
    </section>
  </UContainer>
</template>

<script setup lang="ts">
import type { AnswersType } from '@/types/answers';

const data = defineModel<AnswersType>('data', { required: true });

const { fromAuthor = false } = defineProps<{
  fromAuthor?: boolean;
  companyName: string;
  contactName: string;
  contactEmail: string;
}>();

const editKeyInformation = ref(false);
const editServices = ref(false);
const editIntroduction = ref(false);
const editQuestions = ref(false);
const editRequirements = ref(false);
</script>
