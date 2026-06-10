<template>
  <UContainer class="py-6">
    <h1 class="text-2xl font-semibold mb-6">
      {{ $t("projectDetail.title", { name: data.projectName }) }}
    </h1>
    <section id="key-information" class="mb-8">
      <SectionHeader
        :title="$t('projectDetail.keyInformation')"
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
            <span class="font-bold">{{ $t("projectDetail.companyName") }}</span>
          </div>
          <span class="flex items-center">{{ companyName }}</span>
        </div>

        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-briefcase" class="text-xl text-muted" />
            <span class="font-bold">{{ $t("projectDetail.projectName") }}</span>
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
            <span class="font-bold">{{ $t("projectDetail.startDate") }}</span>
          </div>
          <USelect
            v-if="editKeyInformation"
            v-model="data.startTime"
            :items="startOptions"
            :ui="{ trailingIcon: 'text-normal' }"
          />
          <span v-else class="flex items-center">{{
            translatedStartTime
          }}</span>
        </div>

        <div class="flex justify-between px-4 py-3 min-h-16">
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-dollar-sign" class="text-xl text-muted" />
            <span class="font-bold">{{ $t("projectDetail.budget") }}</span>
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
            <span class="font-bold">{{ $t("projectDetail.location") }}</span>
          </div>

          <span v-if="data.exactLocation === null" class="flex items-center">
            {{ $t("projectDetail.noLocation") }}
          </span>
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
            <span class="font-bold">{{
              $t("projectDetail.contactPerson")
            }}</span>
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
            <span class="font-bold">{{
              $t("projectDetail.companyWebsite")
            }}</span>
          </div>
          <UInput v-if="editKeyInformation" v-model="data.website" />
          <span v-else class="flex items-center">{{ data.website }}</span>
        </div>
      </div>
    </section>

    <section id="introduction" class="mb-8">
      <SectionHeader
        :title="$t('projectDetail.introduction')"
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
        :title="$t('projectDetail.servicesNeeded')"
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
          :placeholder="$t('projectDetail.servicesPlaceholder')"
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
        :title="$t('projectDetail.questions')"
        :editable="fromAuthor"
        edit-inline
        @edit="editQuestions = true"
        @finish-edit="editQuestions = false"
      />
      <ListInput
        v-model="data.questions"
        :editing="editQuestions"
        :add-item-placeholder="$t('projectDetail.addQuestion')"
        :no-items-text="
          fromAuthor
            ? $t('projectDetail.noQuestionsAuthor')
            : $t('projectDetail.noQuestionsVendor')
        "
      />
    </section>

    <section id="requirements">
      <SectionHeader
        :title="$t('projectDetail.requirements')"
        :editable="fromAuthor"
        edit-inline
        @edit="editRequirements = true"
        @finish-edit="editRequirements = false"
      />
      <RequirementsTable
        v-model="data.requirements"
        :editing="editRequirements"
        :no-items-text="
          fromAuthor
            ? $t('projectDetail.noRequirementsAuthor')
            : $t('projectDetail.noRequirementsVendor')
        "
      />
    </section>
  </UContainer>
</template>

<script setup lang="ts">
import type { AnswersType } from "@/types/answers";

const data = defineModel<AnswersType>("data", { required: true });

const { fromAuthor = false } = defineProps<{
  fromAuthor?: boolean;
  companyName: string;
  contactName: string;
  contactEmail: string;
}>();

const { t } = useI18n();

const startOptions = computed(() => [
  { label: t("projectDetail.startOptions.within30"), value: "Within 30 days" },
  { label: t("projectDetail.startOptions.within60"), value: "Within 60 days" },
  { label: t("projectDetail.startOptions.after60"), value: "After 60+ days" },
]);

const translatedStartTime = computed(() => {
  const map: Record<string, string> = {
    "Within 30 days": t("projectDetail.startOptions.within30"),
    "Within 60 days": t("projectDetail.startOptions.within60"),
    "After 60+ days": t("projectDetail.startOptions.after60"),
  };
  return map[data.value.startTime] ?? data.value.startTime;
});

const editKeyInformation = ref(false);
const editServices = ref(false);
const editIntroduction = ref(false);
const editQuestions = ref(false);
const editRequirements = ref(false);
</script>
