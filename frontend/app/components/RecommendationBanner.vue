<template>
  <Transition name="rec-banner">
    <div
      v-if="!dismissed"
      class="flex items-start gap-3 bg-blue-50 border border-blue-200 rounded-2xl px-5 py-4"
    >
      <UIcon
        name="i-lucide-sparkles"
        class="w-5 h-5 text-blue-500 shrink-0 mt-0.5"
      />
      <div class="flex-1 min-w-0">
        <p class="text-sm text-blue-900">
          {{ $t("recommendationBanner.text") }}
          <NuxtLink
            :to="$localePath('/recommendations-policy')"
            class="underline underline-offset-2 hover:text-blue-700 whitespace-nowrap"
          >
            {{ $t("recommendationBanner.learnMore") }}
          </NuxtLink>
        </p>
      </div>
      <UButton
        variant="ghost"
        color="neutral"
        size="xs"
        icon="i-lucide-x"
        class="shrink-0 -mt-0.5 -mr-1 text-blue-500 hover:text-blue-700 hover:bg-blue-100"
        @click="dismiss"
      />
    </div>
  </Transition>
</template>

<script setup lang="ts">
const dismissed = useCookie("recommendation_banner_dismissed", {
  default: () => false,
  maxAge: 60 * 60 * 24 * 365,
  sameSite: "lax",
});

function dismiss() {
  dismissed.value = true;
}
</script>

<style scoped>
.rec-banner-enter-active,
.rec-banner-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease,
    max-height 0.3s ease;
}
.rec-banner-enter-from,
.rec-banner-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
