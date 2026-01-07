<template>
  <div
    v-for="(item, index) in modelValue"
    :key="index"
    class="flex items-center"
  >
    <UIcon v-if="!editing" name="i-lucide-dot" class="w-4 h-4" />
    <UIcon
      v-else
      name="i-lucide-x"
      class="w-4 h-4"
      @click="modelValue = modelValue.filter((_, i) => i !== index)"
    />
    <span v-if="!editing" class="ml-2 px-2.5 py-1.5">{{ item }}</span>
    <UInput
      v-else
      v-model="modelValue[index]"
      variant="soft"
      class="ml-2 w-full"
      :ui="{ base: 'text-base text-normal' }"
      @blur="onItemChange(modelValue[index], index)"
    />
  </div>
  <p v-if="modelValue.length === 0" class="text-muted pl-4.25">
    {{ noItemsText }}
  </p>
  <UInput
    v-if="editing"
    v-model="newItem"
    :placeholder="addItemPlaceholder"
    variant="ghost"
    class="mt-1.5 w-full"
    :ui="{
      base: 'text-base text-normal px-8.5',
    }"
    @keydown.enter="addItem"
  />
</template>

<script setup lang="ts">
const modelValue = defineModel<string[]>({ required: true });
const {
  editing = false,
  addItemPlaceholder = 'Add an Item',
  noItemsText = 'No items',
} = defineProps<{
  editing?: boolean;
  addItemPlaceholder?: string;
  noItemsText?: string;
}>();
const newItem = ref('');

function addItem() {
  if (newItem.value.trim() !== '') {
    modelValue.value = [...modelValue.value, newItem.value.trim()];
    newItem.value = '';
  }
}

function onItemChange(val: string | undefined, index: number) {
  const trimmed = val?.trim() ?? '';

  if (!trimmed) {
    modelValue.value = modelValue.value.filter((_, i) => i !== index);
    return;
  }

  modelValue.value[index] = trimmed;
}
</script>
