<template>
  <UHeader
    title="Vendor Platform"
    class="bg-gray-100"
    :toggle="false"
    :ui="{
      title: 'text-lg font-semibold text-normal',
      header: 'bg-gray-100',
    }"
  >
    <template #right>
      <div class="flex items-center gap-6">
        <nav class="flex items-center gap-6 text-sm font-medium">
          <UButton v-if="!auth.user.value" label="Sign In" to="/sign-in" />
          <UButton v-else label="Dashboard" to="/dashboard" />
        </nav>
      </div>
    </template>

    <!-- <template #body>
      <nav class="flex flex-col gap-2 text-sm font-medium">
        <UButton
          v-if="!auth.user.value"
          label="Sign In"
          to="/sign-in"
          variant="link"
          class="w-fit"
        />
        <UButton
          v-else
          label="Dashboard"
          to="/dashboard"
          class="w-fit"
          variant="link"
        />
        <UButton to="/dashboard/send-review" variant="link">
          Leave a Review
        </UButton>
      </nav>
    </template> -->
  </UHeader>
</template>

<script setup lang="ts">
const auth = useAuth();
</script>
