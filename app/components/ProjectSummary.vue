<template>
  <div class="flex w-full max-w-5xl h-full gap-10 pb-6 text-start">
    <!-- Left Sidebar -->
    <aside class="w-1/3 bg-[#F7A86B] py-10 flex flex-col">
      <h2 class="text-xl font-semibold mb-6 px-3">Your Project Brief</h2>

      <ul class="space-y-4 text-sm px-3 text-gray-800">
        <li class="flex items-start gap-3">
          <UIcon
            name="material-symbols:edit-document-outline-rounded"
            class="text-2xl shrink-0"
          />
          <span class="leading-snug">Review your project details</span>
        </li>
        <li class="flex items-start gap-3">
          <UIcon
            name="material-symbols:mail-outline-rounded"
            class="text-2xl shrink-0"
          />
          <span class="leading-snug"
            >We'll send your project to best-fit vendors</span
          >
        </li>
        <li class="flex items-start gap-3">
          <UIcon
            name="material-symbols:chat-outline-rounded"
            class="text-2xl shrink-0"
          />
          <span class="leading-snug"
            >Receive a response directly through platform</span
          >
        </li>
      </ul>

      <hr class="my-6" />

      <div class="space-y-2 sticky top-0">
        <p class="uppercase text-xs text-gray-700 tracking-wider mb-6 px-3">
          Outline
        </p>
        <button
          v-for="(section, i) in outline"
          :key="i"
          class="block text-left w-full px-3 py-1.5 rounded-md transition"
          :class="[
            currentSection === section
              ? 'bg-[#F4B98A] font-semibold'
              : 'hover:bg-[#F6C6A2]',
          ]"
          @click="scrollToSection(section)"
        >
          {{ section }}
        </button>
      </div>
    </aside>

    <!-- Right Content -->
    <main class="flex-1 bg-white p-10 overflow-y-auto">
      <h1 class="text-2xl font-semibold mb-6">
        Request for {{ data.serviceNeeded }} Services
      </h1>

      <!-- Section: Key Information -->
      <section ref="Key Information" class="mb-8">
        <SectionHeader title="Key Information" @edit="edit('keyInformation')" />

        <InfoTable
          :info="[
            {
              icon: 'mdi:office-building',
              title: 'Company Name',
              value: data.company,
            },
            {
              icon: 'mdi:briefcase-outline',
              title: 'Service Needed',
              value: data.serviceNeeded,
            },
            {
              icon: 'mdi:calendar-outline',
              title: 'Project Start Date',
              value: data.startDate,
            },
            {
              icon: 'mdi:map-marker-outline',
              title: 'Location',
              value: data.location,
            },
            {
              icon: 'mdi:account-outline',
              title: 'Contact Person',
              value: data.contact.name,
              label: data.contact.email,
            },
          ]"
        />
      </section>

      <!-- Section: Introduction -->
      <section ref="Introduction" class="mb-8">
        <SectionHeader title="Introduction" @edit="edit('introduction')" />
        <p class="text-gray-700 leading-relaxed whitespace-pre-line">
          {{ data.introduction }}
        </p>
      </section>

      <!-- Section: Objectives -->
      <section ref="Objectives" class="mb-8">
        <SectionHeader title="Objectives" @edit="edit('objectives')" />
        <ul class="list-disc pl-6 text-gray-700 space-y-1">
          <li v-for="(obj, i) in data.objectives" :key="i">{{ obj }}</li>
        </ul>
        <UButton
          icon="i-heroicons-plus"
          label="Add an objective"
          size="sm"
          variant="outline"
          class="mt-3"
        />
      </section>

      <!-- Section: Services Needed -->
      <section ref="Services Needed" class="mb-8">
        <SectionHeader title="Services Needed" @edit="edit('services')" />
        <div class="border border-gray-300 rounded-lg p-3">
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-gray-500">Primary Service</p>
              <p class="font-medium">{{ data.services.primary }}</p>
            </div>
            <div>
              <p class="text-gray-500">Secondary Service</p>
              <p class="font-medium">{{ data.services.secondary || '-' }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Section: Key Deliverables -->
      <section ref="Key Deliverables" class="mb-8">
        <SectionHeader title="Key Deliverables" @edit="edit('deliverables')" />
        <ul class="list-disc pl-6 text-gray-700 space-y-1">
          <li v-for="(item, i) in data.deliverables" :key="i">{{ item }}</li>
        </ul>
      </section>

      <!-- Section: Questions -->
      <section ref="Questions" class="mb-8">
        <SectionHeader title="Questions" @edit="edit('questions')" />
        <ul class="list-disc pl-6 text-gray-700 space-y-1">
          <li v-for="(q, i) in data.questions" :key="i">{{ q }}</li>
        </ul>
      </section>

      <!-- Section: Requirements -->
      <section ref="Requirements">
        <SectionHeader title="Requirements" @edit="edit('requirements')" />
        <ul class="list-disc pl-6 text-gray-700 space-y-1">
          <li v-for="(r, i) in data.requirements" :key="i">{{ r }}</li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// defineProps({ data: Object });
// Временные данные для UI
const data = ref({
  company: 'Example Inc',
  serviceNeeded: 'Custom Software Development',
  startDate: 'Within 60 days',
  location: 'Near Moscow, Russia',
  contact: { name: 'Example Name', email: 'example@mail.ru' },
  introduction: `We are Example Inc, a dedicated company focused on delivering exceptional services in our field.
Currently, we are facing challenges in streamlining our operations and enhancing user engagement.
To tackle this, we are seeking the expertise of a reliable service provider who can help us develop a custom software solution tailored to our needs.`,
  objectives: [
    'Improve UX design',
    'Optimize database performance',
    'Increase user retention',
  ],
  services: { primary: 'Custom Software Development', secondary: '' },
  deliverables: ['UI/UX Design', 'Mobile Application', 'API Integration'],
  questions: [
    'What is your estimated timeline?',
    'Do you have an in-house development team?',
  ],
  requirements: [
    'NDA required',
    'Weekly project updates',
    'Dedicated project manager',
  ],
});

defineEmits(['edit', 'submit']);

const outline = [
  'Key Information',
  'Introduction',
  'Objectives',
  'Services Needed',
  'Key Deliverables',
  'Questions',
  'Requirements',
];

const currentSection = ref('Key Information');

function scrollToSection(section: string) {
  currentSection.value = section;
  const el = document.querySelector(`[ref='${section}']`);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

function edit(section: string) {
  // Можно открыть модалку с редактированием конкретного блока
  console.log('Edit section:', section);
}
</script>
