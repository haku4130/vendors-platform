<template>
  <div class="flex items-center gap-1">
    <UButton
      v-for="locale in locales"
      :key="locale.code"
      :variant="currentLocale === locale.code ? 'solid' : 'ghost'"
      size="xs"
      @click="switchLocale(locale.code)"
    >
      {{ locale.code.toUpperCase() }}
    </UButton>
  </div>
</template>

<script setup lang="ts">
const { locale: currentLocale, locales } = useI18n();
const switchLocalePath = useSwitchLocalePath();
const router = useRouter();

const switchLocale = (code: string) => {
  router.push(switchLocalePath(code));
};
</script>
