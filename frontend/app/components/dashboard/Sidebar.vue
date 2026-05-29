<template>
  <UDashboardSidebar
    :default-size="25"
    :collapsed-size="0"
    toggle-side="right"
    :ui="{ header: 'border-b border-default bg-gray-100' }"
    class="min-w-fit max-w-md"
  >
    <template #header>
      <NuxtLink
        :to="$localePath('/')"
        class="flex items-center gap-2 pe-4 py-3 text-[1.25rem] font-bold text-blue-600"
      >
        <Logo />
        {{ $t('brandName') }}
      </NuxtLink>
    </template>
    <template #default>
      <NuxtLink :to="$localePath('/dashboard/profile')">
        <UUser
          :name="auth.user.value?.full_name"
          :description="auth.user.value?.company_name"
          :avatar="{
            src: auth.user.value?.logo_url || undefined,
            icon: 'i-lucide-camera',
            class: 'rounded-lg border border-black',
          }"
          size="3xl"
          class="pt-3"
        />
      </NuxtLink>

      <nav class="flex flex-col gap-1 w-full">
        <UButton
          v-for="item in menuItems"
          :key="item.label"
          :to="$localePath(`/dashboard/${item.id}`)"
          :active="route.path.includes(`/dashboard/${item.id}`)"
          variant="ghost"
          class="hover:bg-gray-100"
          active-class="font-semibold bg-gray-100"
          size="lg"
        >
          {{ item.label }}

          <template #trailing>
            <UIcon :name="item.icon" size="20" class="text-sm ml-auto" />
          </template>
        </UButton>
      </nav>
    </template>
    <template #footer>
      <div class="flex justify-between w-full">
        <UButton :to="$localePath('/logout')">
          {{ $t('dashboard.logout') }}
        </UButton>
        <UButton
          :to="$localePath('/dashboard/platform-feedback')"
          variant="link"
        >
          {{ $t('dashboard.platformFeedback') }}
        </UButton>
      </div>
    </template>
  </UDashboardSidebar>
</template>

<script setup lang="ts">
const route = useRoute();
const auth = useAuth();
const { t } = useI18n();

const menuItems = computed(() =>
  auth.user.value?.role === 'company'
    ? [
        {
          id: 'projects',
          label: t('dashboard.menu.projects'),
          icon: 'i-lucide-layers-2',
        },
        {
          id: 'shortlist',
          label: t('dashboard.menu.shortlist'),
          icon: 'i-lucide-bookmark',
        },
        {
          id: 'reviews',
          label: t('dashboard.menu.reviews'),
          icon: 'i-lucide-star',
        },
        {
          id: 'vendors',
          label: t('dashboard.menu.findVendors'),
          icon: 'i-lucide-search',
        },
      ]
    : [
        {
          id: 'projects',
          label: t('dashboard.menu.projects'),
          icon: 'i-lucide-layers-2',
        },
        {
          id: 'portfolio',
          label: t('dashboard.menu.portfolio'),
          icon: 'i-lucide-file-user',
        },
        {
          id: 'reviews',
          label: t('dashboard.menu.reviews'),
          icon: 'i-lucide-star',
        },
        {
          id: 'analytics',
          label: t('dashboard.menu.analytics'),
          icon: 'i-lucide-bar-chart-2',
        },
        {
          id: 'bills',
          label: t('dashboard.menu.bills'),
          icon: 'i-lucide-receipt',
        },
        { id: 'team', label: t('dashboard.menu.team'), icon: 'i-lucide-users' },
      ],
);
</script>
