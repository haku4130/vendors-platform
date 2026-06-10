<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <CookieBanner />
  </UApp>
</template>

<script setup lang="ts">
const auth = useAuth();

onMounted(() => {
  auth.loadUser();
});
</script>
