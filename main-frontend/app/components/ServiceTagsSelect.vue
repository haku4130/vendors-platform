<template>
  <div class="space-y-4">
    <!-- Поисковое селект-поле сверху -->
    <UInputMenu
      v-model="selectedServices"
      :items="items"
      value-key="value"
      multiple
      icon="i-lucide-search"
      :placeholder="placeholder || 'Select services'"
      :ui="{ tagsItem: 'hidden' }"
      class="w-full"
    />
  </div>

  <template v-if="selectedServices.length > 0">
    <USeparator label="Selected Services" class="my-5" />

    <div
      class="flex flex-wrap gap-2 border border-gray-300 rounded-md p-3 min-h-[56px]"
    >
      <div
        v-for="tagId in selectedServices"
        :key="tagId"
        class="px-3 py-1.5 rounded-sm inline-flex items-center gap-1.5 ring ring-inset ring-accented bg-elevated text-default data-disabled:cursor-not-allowed data-disabled:opacity-75 text-xs"
      >
        <span class="truncate">
          {{
            categories
              .flatMap((cat) => cat.tags)
              .find((tag) => tag.id === tagId)?.label || tagId
          }}
        </span>
        <button
          class="inline-flex items-center rounded-xs text-dimmed hover:text-default hover:bg-accented/75 disabled:pointer-events-none transition-colors"
          @click="
            selectedServices = selectedServices.filter((id) => id !== tagId)
          "
        >
          <UIcon name="i-lucide-x" class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  </template>

  <UAccordion :items="accordionItems" class="px-2.5 mt-5">
    <template #body="{ item }">
      <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-2">
        <button
          v-for="tag in item.tags"
          :key="tag.id"
          :class="[
            'px-3 py-1 border rounded-sm text-sm font-medium transition',
            isSelected(tag.id)
              ? 'bg-[#FFB27B] text-black border-[#a68d66] hover:bg-[#eeb488]'
              : 'border-gray-400 text-gray-800 hover:bg-gray-100',
          ]"
          @click="toggleTag(tag.id)"
        >
          {{ tag.label }}
        </button>
      </div>
    </template>
  </UAccordion>
</template>

<script setup lang="ts">
import type { InputMenuItem } from '@nuxt/ui';

defineProps<{
  placeholder?: string;
}>();

interface Tag {
  id: string;
  label: string;
}
interface Category {
  id: string;
  label: string;
  tags: Tag[];
}

const categories: Category[] = [
  {
    id: 'design',
    label: 'Design',
    tags: [
      { id: 'web-design', label: 'Web Design' },
      { id: 'ux-ui-design', label: 'UX/UI Design' },
      { id: 'logo-design', label: 'Logo Design' },
      { id: 'graphic-design', label: 'Graphic Design' },
      { id: 'print-design', label: 'Print Design' },
    ],
  },
  {
    id: 'it-consulting',
    label: 'IT Consulting',
    tags: [
      { id: 'it-strategy', label: 'IT Strategy' },
      { id: 'cloud-consulting', label: 'Cloud Consulting' },
      { id: 'cybersecurity-consulting', label: 'Cybersecurity Consulting' },
      { id: 'devops-consulting', label: 'DevOps Consulting' },
    ],
  },
  {
    id: 'application-development',
    label: 'Application Development',
    tags: [
      { id: 'mobile-app-development', label: 'Mobile App Development' },
      { id: 'web-app-development', label: 'Web App Development' },
      { id: 'backend-api-development', label: 'Backend & API Development' },
      { id: 'frontend-development', label: 'Frontend Development' },
      { id: 'fullstack-development', label: 'Fullstack Development' },
    ],
  },
  {
    id: 'artificial-intelligence',
    label: 'Artificial Intelligence',
    tags: [
      { id: 'ai-development', label: 'AI Development' },
      { id: 'ai-consulting', label: 'AI Consulting' },
      { id: 'generative-ai', label: 'Generative AI' },
      { id: 'ai-agents', label: 'AI Agents' },
      { id: 'machine-learning', label: 'Machine Learning' },
      { id: 'computer-vision', label: 'Computer Vision' },
    ],
  },
  {
    id: 'marketing-digital',
    label: 'Digital Marketing',
    tags: [
      { id: 'social-media-marketing', label: 'Social Media Marketing' },
      { id: 'ppc-advertising', label: 'PPC Advertising' },
      { id: 'seo-services', label: 'SEO Services' },
      { id: 'content-marketing', label: 'Content Marketing' },
      { id: 'email-marketing', label: 'Email Marketing' },
    ],
  },
  {
    id: 'design-graphics',
    label: 'Graphics & Design',
    tags: [
      { id: '3d-modeling', label: '3D Modeling' },
      { id: 'motion-graphics', label: 'Motion Graphics' },
      { id: 'illustration', label: 'Illustration' },
      { id: 'branding', label: 'Branding' },
      { id: 'ui-icon-design', label: 'UI / Icon Design' },
    ],
  },
];

function buildInputMenuItems(categories: Category[]): InputMenuItem[] {
  const items: InputMenuItem[] = [];

  categories.forEach((cat) => {
    // добавить метку-категорию
    items.push({ type: 'label', label: cat.label });
    // добавить теги категории
    cat.tags.forEach((tag) => {
      items.push({
        label: tag.label,
        value: tag.id, // желательно добавить id как value, чтобы удобнее v-model
      });
    });
    // разделитель
    items.push({ type: 'separator' });
  });

  // Удалим последний разделитель, если не нужен
  if (items.length > 0 && items[items.length - 1].type === 'separator') {
    items.pop();
  }

  return items;
}

const items = ref<InputMenuItem[]>(buildInputMenuItems(categories));
const selectedServices = defineModel<string[]>();

const accordionItems = computed(() => {
  return categories.map((cat) => ({
    label: cat.label,
    tags: cat.tags,
  }));
});

function toggleTag(tagId: string) {
  const idx = selectedServices.value.indexOf(tagId);
  if (idx === -1) {
    selectedServices.value.push(tagId);
  } else {
    selectedServices.value.splice(idx, 1);
  }
}

function isSelected(tagId: string) {
  return selectedServices.value.includes(tagId);
}
</script>
