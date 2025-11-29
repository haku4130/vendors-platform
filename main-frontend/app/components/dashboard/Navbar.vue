<template>
  <UDashboardNavbar title="Dashboard" class="bg-gray-100">
    <template #right>
      <div class="flex gap-6">
        <UButton to="/send-review" variant="link"> Leave a Review </UButton>
        <UButton
          class="w-fit"
          to="/dashboard/profile"
          :variant="
            useRoute().path === '/dashboard/profile' ? 'solid' : 'outline'
          "
        >
          Profile
        </UButton>
      </div>
    </template>
  </UDashboardNavbar>
</template>
