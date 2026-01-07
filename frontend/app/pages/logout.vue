<template>
  <div>Logging out...</div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['auth'],
});

const auth = useAuth();

onMounted(() => {
  auth.logout();
  const toast = useToast();
  toast.add({
    title: 'Logged out',
    description: 'You have been successfully logged out.',
    color: 'success',
  });
  navigateTo('/sign-in');
});
</script>
