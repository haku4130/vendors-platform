<template>
  <div class="flex items-center gap-2 mb-2">
    <h2 class="text-lg font-bold">{{ title }}</h2>
    <UButton
      v-if="editable && (!editing || !editInline)"
      icon="i-lucide-square-pen"
      variant="ghost"
      color="neutral"
      @click="
        $emit('edit');
        editing = true;
      "
    />
    <UButton
      v-if="editable && editing && editInline"
      icon="i-lucide-check"
      variant="ghost"
      color="neutral"
      @click="
        $emit('finish-edit');
        editing = false;
      "
    />
  </div>
</template>

<script setup lang="ts">
const { editable = false, editInline = false } = defineProps<{
  title: string;
  editable?: boolean;
  editInline?: boolean;
}>();
const editing = ref(false);
defineEmits(['edit', 'finish-edit']);
</script>
