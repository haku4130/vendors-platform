<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">{{ $t('content.editPage') }}: {{ slug }}</h1>
      <div class="flex gap-3">
        <NuxtLink :to="$localePath(`/${slug}`)">
          <UButton variant="outline" icon="i-lucide-eye">{{ $t('content.preview') }}</UButton>
        </NuxtLink>
        <UButton icon="i-lucide-save" :loading="saving" @click="save">
          {{ $t('content.save') }}
        </UButton>
      </div>
    </div>

    <UTabs :items="tabs" class="w-full">
      <template #ru>
        <div class="mt-4">
          <p class="text-sm text-muted mb-2">Русский</p>
          <UEditor v-model="ruContent" class="min-h-[500px]" />
        </div>
      </template>
      <template #en>
        <div class="mt-4">
          <p class="text-sm text-muted mb-2">English</p>
          <UEditor v-model="enContent" class="min-h-[500px]" />
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
