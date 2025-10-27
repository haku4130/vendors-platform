<template>
  <div class="flex">
    <DashboardSidebar
      :items="menuItems"
      :selected="activeTab"
      @select="handleSelect"
    />

    <!-- Main content -->
    <main class="flex-1 p-8">
      <!-- <h1 class="text-2xl font-semibold mb-6">{{ activeTabLabel }}</h1> -->

      <div v-if="activeTab === 'projects'">
        <p class="text-gray-700">
          <ProjectsSection />
        </p>
      </div>

      <div v-else-if="activeTab === 'messages'">
        <p class="text-gray-700">
          <MessagesSection />
        </p>
      </div>

      <div v-else-if="activeTab === 'shortlist'">
        <p class="text-gray-700">
          <ShortlistSection />
        </p>
      </div>

      <div v-else-if="activeTab === 'reviews'">
        <p class="text-gray-700">
          <ReviewsSection />
        </p>
      </div>

      <div v-else>
        <p class="text-gray-500">Select a section from the sidebar.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import ProjectsSection from '@/components/dashboard/ProjectsSection.vue';
import DashboardSidebar from '@/components/dashboard/DashboardSidebar.vue';
import MessagesSection from '@/components/dashboard/MessagesSection.vue';
import ShortlistSection from '@/components/dashboard/ShortlistSection.vue';
import ReviewsSection from '@/components/dashboard/ReviewsSection.vue';

// Активная вкладка
const activeTab = ref('projects');

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

// Подпись текущей вкладки
// const activeTabLabel = computed(
//  () => menuItems.find((i) => i.id === activeTab.value)?.label || ''
// );

// Обработка выбора
function handleSelect(tab) {
  activeTab.value = tab;
}
</script>
