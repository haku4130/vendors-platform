<template>
  <UDashboardSidebar
    :default-size="25"
    :collapsed-size="0"
    toggle-side="right"
    :ui="{ header: 'border-b border-default bg-gray-100' }"
    class="min-w-fit max-w-md"
  >
    <template #header>
      <NuxtLink to="/">
        <h2 class="text-lg font-semibold px-4 py-3">Vendor Platform</h2>
      </NuxtLink>
    </template>
    <template #default>
      <NuxtLink to="/dashboard/profile">
        <UUser
          :name="auth.user.value?.full_name"
          :description="auth.user.value?.company_name"
          :avatar="{
            src: auth.user.value?.logo_url || undefined,
            icon: 'i-lucide-camera',
            class: 'rounded-lg border border-black',
          }"
          size="3xl"
          class="px-4 pt-3"
        />
      </NuxtLink>

      <nav class="flex flex-col gap-1 w-full">
        <UButton
          v-for="item in menuItems"
          :key="item.label"
          :to="`/dashboard/${item.id}`"
          :active="route.path.includes(`/dashboard/${item.id}`)"
          variant="ghost"
          class="hover:bg-gray-100"
          active-class="font-semibold bg-gray-100"
          size="lg"
        >
          <template #leading>
            <UIcon :name="item.icon" size="20" />
          </template>

          {{ item.label }}

          <template #trailing>
            <span class="text-sm ml-auto"> 0 </span>
          </template>
        </UButton>
      </nav>
    </template>
    <template #footer>
      <UButton to="/logout"> Log Out </UButton>
    </template>
  </UDashboardSidebar>
</template>

<script setup lang="ts">
const route = useRoute();
const auth = useAuth();

const menuItems =
  auth.user.value?.role === 'company'
    ? [
        {
          id: 'projects',
          label: 'Projects',
          icon: 'i-lucide-layers-2',
        },
        {
          id: 'messages',
          label: 'Messages',
          icon: 'i-lucide-message-square-text',
        },
        {
          id: 'shortlist',
          label: 'Shortlist',
          icon: 'i-lucide-bookmark',
        },
        { id: 'reviews', label: 'Reviews', icon: 'i-lucide-star' },
      ]
    : [
        {
          id: 'projects',
          label: 'Projects',
          icon: 'i-lucide-layers-2',
        },
        {
          id: 'messages',
          label: 'Messages',
          icon: 'i-lucide-message-square-text',
        },
        { id: 'portfolio', label: 'Portfolio', icon: 'i-lucide-file-user' },
        { id: 'reviews', label: 'Reviews', icon: 'i-lucide-star' },
        { id: 'analytics', label: 'Analytics', icon: 'i-lucide-bar-chart-2' },
        { id: 'bills', label: 'Bills', icon: 'i-lucide-receipt' },
        { id: 'team', label: 'Team', icon: 'i-lucide-users' },
      ];
</script>
