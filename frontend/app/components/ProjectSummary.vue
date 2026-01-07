<template>
  <div class="flex w-full max-w-5xl h-full gap-10 pb-6 text-start">
    <aside class="w-1/3 py-6 flex flex-col">
      <h2 class="text-xl font-semibold mb-6 px-3">Your Project Brief</h2>

      <ul class="space-y-4 text-sm px-3 text-gray-800">
        <li class="flex items-start gap-3">
          <UIcon name="i-lucide-file-pen" class="text-2xl shrink-0" />
          <span class="leading-snug">Review your project details</span>
        </li>
        <li class="flex items-start gap-3">
          <UIcon name="i-lucide-mail" class="text-2xl shrink-0" />
          <span class="leading-snug"
            >We'll send your project to best-fit vendors</span
          >
        </li>
        <li class="flex items-start gap-3">
          <UIcon
            name="i-lucide-message-square-text"
            class="text-2xl shrink-0"
          />
          <span class="leading-snug"
            >Receive a response directly through platform</span
          >
        </li>
      </ul>

      <USeparator color="primary" class="my-6" />

      <div class="space-y-2 sticky top-0">
        <p class="uppercase text-xs text-gray-700 tracking-wider mb-6 px-3">
          Outline
        </p>
        <button
          v-for="(section, i) in links"
          :key="i"
          class="block text-left w-full px-3 py-1.5 rounded-md transition"
          :class="[
            currentSection === section.id
              ? 'bg-[#F4B98A] font-semibold'
              : 'hover:bg-[#F6C6A2]',
          ]"
          @click="scrollToSection(section.id)"
        >
          {{ section.text }}
        </button>
      </div>
    </aside>

    <ProjectDetail
      v-model:data="answers"
      :company-name="auth.user.value?.company_name || ''"
      :contact-email="auth.user.value?.email || ''"
      :contact-name="auth.user.value?.full_name || ''"
      from-author
      class="bg-white"
    />
  </div>
</template>

<script setup lang="ts">
import type { AnswersType } from '@/types/answers';

const auth = useAuth();

const answers = defineModel<AnswersType>({ required: true });

const links = [
  {
    id: 'key-information',
    text: 'Key Information',
  },
  {
    id: 'introduction',
    text: 'Introduction',
  },
  {
    id: 'services',
    text: 'Services Needed',
  },
  {
    id: 'questions',
    text: 'Questions',
  },
  {
    id: 'requirements',
    text: 'Requirements',
  },
];

const currentSection = ref('key-information');

function scrollToSection(section: string) {
  currentSection.value = section;
  const el = document.getElementById(section);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' });
  }
}

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

      if (visible[0]) {
        currentSection.value = visible[0].target.id;
      }
    },
    {
      rootMargin: '0px 0px -90% 0px',
    }
  );

  links.forEach((link) => {
    const el = document.getElementById(link.id);
    if (el) observer.observe(el);
  });

  onBeforeUnmount(() => {
    observer.disconnect();
  });
});
</script>
