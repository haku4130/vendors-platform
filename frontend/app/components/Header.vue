<template>
  <UHeader
    title="Vendor Platform"
    class="bg-gray-100"
    :ui="{ title: 'text-lg font-semibold text-normal' }"
  >
    <template #right>
      <div class="flex items-center gap-6">
        <nav class="flex items-center gap-6 text-sm font-medium">
          <UButton to="/send-review" variant="link"> Leave a Review </UButton>
          <UButton v-if="!auth.user.value" label="Sign In" to="/sign-in" />
          <UButton v-else label="Dashboard" to="/dashboard" />
        </nav>
      </div>
    </template>
  </UHeader>
</template>

<script setup lang="ts">
const auth = useAuth();
</script>
