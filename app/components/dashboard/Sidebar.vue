<template>
  <UDashboardSidebar
    :default-size="25"
    :collapsed-size="0"
    toggle-side="right"
    :ui="{ header: 'border-b border-default' }"
    class="min-w-fit max-w-md"
  >
    <template #header>
      <NuxtLink to="/">
        <h2 class="text-lg font-semibold px-4 py-3">Vendor Platform</h2>
      </NuxtLink>
    </template>
    <template #default>
      <!-- Аватар -->
      <UUser
        name="Osipov Andrey"
        description="Acme Corp"
        :avatar="{
          src: 'https://github.com/haku4130.png',
          icon: 'mdi:camera-outline',
          class: 'rounded-lg border border-black',
        }"
        size="3xl"
        class="px-4 pt-3"
      />

      <!-- Кнопка редактирования -->
      <!-- <div class="pl-4">
        <UButton size="sm"> Edit Profile </UButton>
      </div> -->

      <!-- Навигация -->
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
            <span class="text-sm ml-auto">
              {{ item.count }}
            </span>
          </template>
        </UButton>
      </nav>
    </template>
    <template #footer>
      <UButton> Profile </UButton>
    </template>
  </UDashboardSidebar>
</template>

<script setup lang="ts">
const route = useRoute();

// Список вкладок для компании
const menuItems = [
  { id: 'projects', label: 'Projects', icon: 'mdi:layers-outline', count: 0 },
  {
    id: 'messages',
    label: 'Messages',
    icon: 'mdi:message-reply-text-outline',
    count: 0,
  },
  {
    id: 'shortlist',
    label: 'Shortlist',
    icon: 'mdi:bookmark-outline',
    count: 0,
  },
  { id: 'reviews', label: 'Reviews', icon: 'mdi:star-outline', count: 0 },
];
</script>
