<template>
  <div class="max-w-3xl">
    <div
      v-if="project?.is_archived"
      class="mb-4 flex items-center gap-2 px-4 py-3 rounded-lg bg-amber-50 border border-amber-200 text-amber-800"
    >
      <UIcon name="i-lucide-archive" class="w-5 h-5 shrink-0" />
      <span class="font-medium">{{ $t('dashboard.projects.archived') }}</span>
    </div>

    <ProjectDetail
      v-if="project && answers"
      :data="answers"
      :company-name="project.owner.company_name"
      :contact-email="project.owner.email"
      :contact-name="project.owner.full_name"
    />

    <div
      v-if="isOwner && project && !project.is_archived"
      class="px-6 pb-6 flex justify-end"
    >
      <UButton
        color="neutral"
        variant="outline"
        icon="i-lucide-archive"
        :label="$t('dashboard.projects.archiveProject')"
        :loading="archiving"
        @click="confirmArchive = true"
      />
    </div>

    <UModal v-model:open="confirmArchive">
      <template #content>
        <div class="p-6 space-y-4">
          <h3 class="text-lg font-semibold">
            {{ $t('dashboard.projects.archiveConfirmTitle') }}
          </h3>
          <p class="text-muted">
            {{ $t('dashboard.projects.archiveConfirmDesc') }}
          </p>
          <div class="flex justify-end gap-3">
            <UButton
              variant="ghost"
              :label="$t('common.cancel')"
              @click="confirmArchive = false"
            />
            <UButton
              color="warning"
              icon="i-lucide-archive"
              :label="$t('dashboard.projects.archiveProject')"
              :loading="archiving"
              @click="doArchive"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import {
  projectsGetProjectDetail,
  projectsArchiveProject,
} from '~/generated/api';
import type { ProjectPublic } from '~/generated/api';
import type { AnswersType } from '@/types/answers';

const { projectId } = defineProps<{
  projectId: string;
}>();

const auth = useAuth();
const toast = useToast();
const router = useRouter();

const project = ref<ProjectPublic | null>(null);
const confirmArchive = ref(false);
const archiving = ref(false);

const isOwner = computed(() => auth.user.value?.id === project.value?.owner.id);

onMounted(async () => {
  const res = await projectsGetProjectDetail({
    path: { project_id: projectId as string },
  });

  if (res.error) {
    throw createError({
      statusCode: 404,
      message: 'Project does not exist',
      fatal: true,
    });
  }

  project.value = res.data!;
});

const answers = computed<AnswersType | null>(() => {
  if (!project.value) return null;

  return {
    projectName: project.value.title,
    projectIntroduction: project.value.description ?? '',
    startTime: project.value.start_date ?? '',
    exactLocation: project.value.location ?? null,
    website: project.value.website ?? '',
    servicesNeeded: project.value.services ?? [],
    budget: project.value.budget ?? 0,
    questions: project.value.questions ?? [],
    requirements: project.value.requirements ?? [],
  };
});

async function doArchive() {
  archiving.value = true;
  const res = await projectsArchiveProject({
    path: { project_id: projectId },
  });
  archiving.value = false;
  confirmArchive.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error),
      color: 'error',
    });
  } else {
    project.value = res.data!;
    toast.add({
      title: 'Project archived',
      description: 'The project has been archived.',
      color: 'success',
    });
    router.push('/dashboard/projects');
  }
}
</script>
