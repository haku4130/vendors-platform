<template>
  <UDashboardPanel resizable>
    <template #header>
      <UDashboardNavbar title="Dashboard" />
    </template>

    <template #body>
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
    </template>
  </UDashboardPanel>
</template>

<script setup lang="ts">
import ProjectsSection from '@/components/dashboard/ProjectsSection.vue';
import MessagesSection from '@/components/dashboard/MessagesSection.vue';
import ShortlistSection from '@/components/dashboard/ShortlistSection.vue';
import ReviewsSection from '@/components/dashboard/ReviewsSection.vue';

definePageMeta({
  layout: 'dashboard',
});

// Активная вкладка
const activeTab = useState('activeTab');
</script>
