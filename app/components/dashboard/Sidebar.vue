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
        <button
          v-for="item in menuItems"
          :key="item.label"
          :class="[
            'flex items-center justify-between w-full py-2 px-4 rounded-lg font-medium transition',
            activeTab === item.id
              ? 'bg-gray-100 text-black font-semibold'
              : 'hover:bg-gray-100 text-gray-800',
          ]"
          @click="handleSelect(item.id)"
        >
          <div class="flex items-center gap-3">
            <UIcon :name="item.icon" size="20" />
            <span>{{ item.label }}</span>
          </div>
          <span v-if="item.count !== undefined" class="text-sm">
            {{ item.count }}
          </span>
        </button>
      </nav>
    </template>
    <template #footer>
      <UButton> Profile </UButton>
    </template>
  </UDashboardSidebar>
</template>

<script setup lang="ts">
// Список вкладок для компании
const menuItems = [
  { id: 'projects', label: 'Projects', icon: 'mdi:layers-outline', count: 0 },
  { id: 'messages', label: 'Messages', icon: 'mdi:message-outline', count: 0 },
  {
    id: 'shortlist',
    label: 'Shortlist',
    icon: 'mdi:bookmark-outline',
    count: 0,
  },
  { id: 'reviews', label: 'Reviews', icon: 'mdi:star-outline', count: 0 },
];

// Активная вкладка
const activeTab = useState('activeTab', () => 'projects');

// Обработка выбора
function handleSelect(tab: string) {
  activeTab.value = tab;
}
</script>
