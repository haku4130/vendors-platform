<template>
  <UDashboardNavbar :title="$t('dashboard.title')" class="bg-gray-100" toggle-side="right">
    <template #right>
      <div class="hidden lg:flex items-center gap-4">
        <LangSwitcher />
        <UButton
          class="w-fit"
          :to="$localePath('/dashboard/profile')"
          :variant="
            useRoute().path.includes('/dashboard/profile') ? 'solid' : 'outline'
          "
        >
          {{ $t('dashboard.menu.profile') }}
        </UButton>
      </div>
    </template>
  </UDashboardNavbar>
</template>
