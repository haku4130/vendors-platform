<template>
  <ProjectDetail
    v-if="project && answers"
    :data="answers"
    :company-name="project.owner.company_name"
    :contact-email="project.owner.email"
    :contact-name="project.owner.full_name"
    class="max-w-3xl"
  />
</template>

<script setup lang="ts">
import { projectsGetProjectDetail } from '~/generated/api';
import type { ProjectPublic } from '~/generated/api';
import type { AnswersType } from '@/types/answers';

const { projectId } = defineProps<{
  projectId: string;
}>();
const project = ref<ProjectPublic | null>(null);

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
</script>
