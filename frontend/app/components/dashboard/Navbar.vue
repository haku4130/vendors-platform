<template>
  <UDashboardNavbar title="Dashboard" class="bg-gray-100" toggle-side="right">
    <template #right>
      <div class="hidden lg:flex gap-6">
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
