<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">
        {{ $t('content.editPage') }}: {{ slug }}
      </h1>
      <div class="flex gap-3">
        <NuxtLink :to="$localePath(`/${slug}`)">
          <UButton variant="outline" icon="i-lucide-eye">{{
            $t('content.preview')
          }}</UButton>
        </NuxtLink>
        <UButton
          icon="i-lucide-save"
          variant="solid"
          :loading="saving"
          @click="save"
        >
          {{ $t('content.save') }}
        </UButton>
      </div>
    </div>

    <UTabs :items="tabs" class="w-full">
      <template #ru>
        <div class="mt-4">
          <UEditor
            v-slot="{ editor }"
            v-model="ruContent"
            class="min-h-[500px] border border-default rounded-lg overflow-hidden"
            :ui="{ content: 'p-3' }"
          >
            <UEditorToolbar
              :editor="editor"
              :items="toolbarItems"
              class="border-b border-default px-2 py-1"
            />
          </UEditor>
        </div>
      </template>
      <template #en>
        <div class="mt-4">
          <UEditor
            v-slot="{ editor }"
            v-model="enContent"
            class="min-h-[500px] border border-default rounded-lg overflow-hidden"
            :ui="{ content: 'p-3' }"
          >
            <UEditorToolbar
              :editor="editor"
              :items="toolbarItems"
              class="border-b border-default px-2 py-1"
            />
          </UEditor>
        </div>
      </template>
    </UTabs>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'superuser'],
});

const route = useRoute();
const slug = computed(() => route.params.slug as string);
const toast = useToast();
const { t } = useI18n();

const tabs = [
  { label: 'RU', slot: 'ru' },
  { label: 'EN', slot: 'en' },
];

const toolbarItems = [
  [
    { kind: 'heading', level: 1, icon: 'i-lucide-heading-1' },
    { kind: 'heading', level: 2, icon: 'i-lucide-heading-2' },
    { kind: 'heading', level: 3, icon: 'i-lucide-heading-3' },
  ],
  [
    { kind: 'mark', mark: 'bold', icon: 'i-lucide-bold' },
    { kind: 'mark', mark: 'italic', icon: 'i-lucide-italic' },
    { kind: 'mark', mark: 'strike', icon: 'i-lucide-strikethrough' },
  ],
  [
    { kind: 'bulletList', icon: 'i-lucide-list' },
    { kind: 'orderedList', icon: 'i-lucide-list-ordered' },
  ],
  [
    { kind: 'blockquote', icon: 'i-lucide-quote' },
    { kind: 'codeBlock', icon: 'i-lucide-code' },
  ],
  [{ kind: 'link', icon: 'i-lucide-link' }],
  [
    { kind: 'undo', icon: 'i-lucide-undo' },
    { kind: 'redo', icon: 'i-lucide-redo' },
  ],
];

const { data } = await useFetch<{ ru: string; en: string }>(
  () => `/content-api/${slug.value}`,
);

const ruContent = ref(data.value?.ru ?? '');
const enContent = ref(data.value?.en ?? '');

const saving = ref(false);

async function save() {
  saving.value = true;
  try {
    await $fetch(`/content-api/${slug.value}`, {
      method: 'POST',
      body: { ru: ruContent.value, en: enContent.value },
    });
    toast.add({ title: t('content.saved'), color: 'success' });
  } catch {
    toast.add({ title: t('content.saveError'), color: 'error' });
  } finally {
    saving.value = false;
  }
}
</script>
