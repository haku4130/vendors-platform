<template>
  <Transition name="cookie-banner">
    <div
      v-if="!accepted"
      class="fixed bottom-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-t border-gray-700"
    >
      <div
        class="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex flex-col sm:flex-row items-start sm:items-center gap-4"
      >
        <UIcon
          name="i-lucide-cookie"
          class="w-5 h-5 text-amber-400 shrink-0 mt-0.5 sm:mt-0"
        />
        <p class="text-sm text-gray-200 flex-1">
          {{ $t("cookieBanner.text") }}&nbsp;<NuxtLink
            :to="$localePath('/privacy')"
            class="text-blue-400 hover:text-blue-300 underline underline-offset-2"
            >{{ $t("cookieBanner.privacyLink") }}</NuxtLink
          >.
        </p>
        <UButton size="sm" class="shrink-0" @click="accept">
          {{ $t("cookieBanner.accept") }}
        </UButton>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
const accepted = useCookie("cookie_consent", {
  default: () => false,
  maxAge: 60 * 60 * 24 * 365,
  sameSite: "lax",
});

function accept() {
  accepted.value = true;
}
</script>

<style scoped>
.cookie-banner-enter-active,
.cookie-banner-leave-active {
  transition:
    transform 0.3s ease,
    opacity 0.3s ease;
}
.cookie-banner-enter-from,
.cookie-banner-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
