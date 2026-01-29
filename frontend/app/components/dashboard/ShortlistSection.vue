<template>
  <section class="bg-vendor-gradient p-6 rounded-2xl">
    <h1 class="text-2xl font-semibold text-gray-900">Shortlist</h1>
    <p class="mt-1 text-gray-900">
      Your favorite vendors saved for quick access.
    </p>
  </section>
  <div
    v-if="Object.values(shortlistCounts).every((count) => count === 0)"
    class="space-y-8"
  >
    <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold mb-6">How it works</h3>

        <UStepper
          v-model="active"
          color="neutral"
          orientation="vertical"
          :items="items"
          class="w-full"
        />
      </div>

      <div
        class="bg-white rounded-2xl p-6 shadow-sm flex flex-col justify-center max-h-fit"
      >
        <h3 class="text-lg font-semibold mb-4">
          You haven’t picked your favorites yet!
        </h3>
        <UButton size="xl" class="w-fit" to="/dashboard/projects">
          Find a Partner
        </UButton>
      </div>
    </section>
  </div>
  <div v-else class="space-y-6">
    <div v-if="loading" class="flex justify-center items-center min-h-[200px]">
      <div class="text-center">
        <UIcon
          name="i-lucide-loader-2"
          class="w-8 h-8 animate-spin mx-auto mb-4"
        />
        <p class="text-muted">Loading shortlist...</p>
      </div>
    </div>

    <div v-else-if="projects.length === 0">
      <UEmpty
        icon="i-lucide-bookmark"
        title="No projects yet"
        description="Create a project first, then you can add vendors to your shortlist."
        class="w-fit mx-auto"
      />
    </div>

    <div v-else class="space-y-8">
      <section v-for="project in projects" :key="project.id">
        <div
          v-if="shortlistCounts[project.id]"
          class="bg-white rounded-2xl p-6 shadow-sm"
        >
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-semibold">{{ project.title }}</h3>
              <p class="text-sm text-muted">
                {{ shortlistCounts[project.id] || 0 }} vendor(s) in shortlist
              </p>
            </div>
            <UButton
              :to="`/dashboard/projects/${project.id}/explore`"
              variant="outline"
              size="sm"
            >
              Find More Vendors
            </UButton>
          </div>

          <div v-if="loadingShortlists[project.id]" class="py-8 text-center">
            <UIcon
              name="i-lucide-loader-2"
              class="w-6 h-6 animate-spin mx-auto"
            />
          </div>

          <div
            v-else-if="shortlistedVendors[project.id]?.length"
            class="space-y-4"
          >
            <VendorCard
              v-for="vendor in shortlistedVendors[project.id]"
              :key="vendor.id"
              :vendor="vendor"
              :current-project-id="project.id"
              request-id=""
              :initially-shortlisted="true"
              :on-shortlist-changed="() => loadShortlistForProject(project.id)"
              @shortlist-changed="() => loadShortlistForProject(project.id)"
            />
          </div>

          <UEmpty
            v-else
            icon="i-lucide-bookmark"
            title="No vendors in shortlist"
            description="Browse vendors and add them to your shortlist for this project."
            class="w-fit mx-auto py-8"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { StepperItem } from '@nuxt/ui';
import type {
  ProjectWithIncomingCount,
  VendorProfilePublic,
} from '~/generated/api';
import {
  projectsListMyProjects,
  shortlistGetShortlistedVendors,
} from '~/generated/api';

const items = ref<StepperItem[]>([
  {
    title: 'Start a Project',
    description: 'Create a brief describing your needs and goals.',
  },
  {
    title: 'Get Matched',
    description:
      'We’ll suggest the best-fit vendors based on your project details.',
  },
  {
    title: 'Shortlist & Decide',
    description:
      'Compare proposals, pick your favorites, and choose who to work with.',
  },
]);

const active = ref(0);

onMounted(() => {
  setInterval(() => {
    active.value = (active.value + 1) % items.value.length;
  }, 1500);
  loadProjects();
});

const toast = useToast();
const loading = ref(true);
const projects = ref<ProjectWithIncomingCount[]>([]);
const shortlistedVendors = ref<Record<string, VendorProfilePublic[]>>({});
const loadingShortlists = ref<Record<string, boolean>>({});
const shortlistCounts = ref<Record<string, number>>({});

async function loadProjects() {
  loading.value = true;
  const res = await projectsListMyProjects();
  loading.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Failed to load projects'),
      color: 'error',
    });
    return;
  }

  projects.value = (res.data ?? []) as ProjectWithIncomingCount[];

  // Load shortlists for each project
  for (const project of projects.value) {
    loadShortlistForProject(project.id);
  }
}

async function loadShortlistForProject(projectId: string) {
  loadingShortlists.value[projectId] = true;

  const res = await shortlistGetShortlistedVendors({
    path: {
      project_id: projectId,
    },
  });

  loadingShortlists.value[projectId] = false;

  if (res.error) {
    console.error('Failed to load shortlist:', res.error);
    shortlistedVendors.value[projectId] = [];
    shortlistCounts.value[projectId] = 0;
    return;
  }

  shortlistedVendors.value[projectId] = res.data || [];
  shortlistCounts.value[projectId] = (res.data || []).length;
}
</script>
