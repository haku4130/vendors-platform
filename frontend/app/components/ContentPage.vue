<template>
  <div class="bg-white min-h-screen">
    <Header />
    <main class="max-w-4xl mx-auto px-6 py-16">
      <div v-if="pending" class="flex justify-center py-24">
        <UIcon
          name="i-lucide-loader-2"
          class="w-8 h-8 animate-spin text-muted"
        />
      </div>
      <div v-else class="prose prose-slate max-w-none" v-html="content"></div>
    </main>
    <NuxtLink
      v-if="isSuperuser"
      :to="$localePath(`/dashboard/content/${slug}`)"
      class="fixed bottom-6 right-6"
    >
      <UButton icon="i-lucide-pencil" size="lg" class="shadow-lg">
        {{ $t('content.edit') }}
      </UButton>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ slug: string }>();

const { locale } = useI18n();
const auth = useAuth();

const isSuperuser = computed(() => auth.user.value?.is_superuser === true);

const { data, pending } = await useFetch<{ ru: string; en: string }>(
  `/content-api/${props.slug}`,
);

const content = computed(() => {
  if (!data.value) return '';
  return locale.value === 'ru' ? data.value.ru : data.value.en;
});
</script>
