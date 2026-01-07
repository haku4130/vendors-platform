<template>
  <div class="space-y-4">
    <UInputMenu
      v-model="selectedServices"
      :items="items"
      value-key="value"
      multiple
      icon="i-lucide-search"
      :placeholder="placeholder || 'Select services'"
      :disabled="selectedServices.length > maxSelected - 1"
      :ui="{ tagsItem: 'hidden' }"
      class="w-full"
    />
    <div v-if="errors[0]" class="text-error text-start mt-2">
      {{ errors[0]?.message }}
    </div>
    <div v-else class="text-muted text-start mt-2">
      Select up to {{ maxSelected }} services
    </div>
  </div>

  <template v-if="selectedServices && selectedServices.length > 0">
    <USeparator
      :label="`Selected Services (${selectedServices.length}/${maxSelected})`"
      class="my-5"
    />

    <div
      class="flex flex-wrap gap-2 border border-gray-300 rounded-md p-3 min-h-[56px]"
      :class="{ 'border-red-700': errors.length > 0 }"
    >
      <div
        v-for="tag in selectedServices"
        :key="tag.id"
        class="px-3 py-1.5 rounded-sm inline-flex items-center gap-1.5 ring ring-inset ring-accented bg-elevated text-default data-disabled:cursor-not-allowed data-disabled:opacity-75 text-xs"
      >
        <span class="truncate">
          {{ tag.label }}
        </span>
        <button
          class="inline-flex items-center rounded-xs text-dimmed hover:text-default hover:bg-accented/75 disabled:pointer-events-none transition-colors"
          @click="toggleTag(tag)"
        >
          <UIcon name="i-lucide-x" class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  </template>

  <UAccordion :items="categories" class="px-0 mt-5">
    <template #body="{ item }">
      <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-2">
        <button
          v-for="tag in item.services"
          :key="tag.id"
          :disabled="
            !isSelected(tag.id) && selectedServices.length >= maxSelected
          "
          :class="[
            'px-3 py-1 border rounded-sm text-sm font-medium disabled:cursor-not-allowed disabled:opacity-75 transition',
            isSelected(tag.id)
              ? 'bg-vendor-gradient text-black border-[#a68d66] hover:bg-[#eeb488]'
              : 'border-gray-400 text-gray-800 hover:bg-gray-100',
          ]"
          @click="toggleTag(tag)"
        >
          {{ tag.label }}
        </button>
      </div>
    </template>
  </UAccordion>
</template>

<script setup lang="ts">
import type { InputMenuItem, FormError } from '@nuxt/ui';
import { catalogListCategories } from '~/generated/api';
import type { CategoryPublic, ServicePublicShort } from '~/generated/api';

const {
  placeholder = 'Search here',
  errors,
  maxSelected = 5,
} = defineProps<{
  placeholder?: string;
  maxSelected?: number;
  errors: FormError<string>[];
}>();

const selectedServices = defineModel<ServicePublicShort[]>({ required: true });

const { data: categories } = await catalogListCategories();

const items = ref<InputMenuItem[]>(buildInputMenuItems(categories));

function buildInputMenuItems(
  categories: CategoryPublic[] | undefined
): InputMenuItem[] {
  if (!categories) {
    return [];
  }

  const items: InputMenuItem[] = [];

  categories.forEach((cat) => {
    items.push({ type: 'label', label: cat.label });
    cat.services.forEach((service) => {
      items.push({
        label: service.label,
        value: service,
      });
    });
    items.push({ type: 'separator' });
  });

  // Remove the last separator
  if (items.length > 0) {
    items.pop();
  }

  return items;
}

function toggleTag(tag: ServicePublicShort) {
  if (isSelected(tag.id)) {
    selectedServices.value = selectedServices.value.filter(
      (t) => t.id !== tag.id
    );
  } else {
    selectedServices.value = [...selectedServices.value, tag];
  }
}

function isSelected(tagId: string) {
  return selectedServices.value.some((tag) => tag.id === tagId);
}
</script>
