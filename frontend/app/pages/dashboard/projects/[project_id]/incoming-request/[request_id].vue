<template>
  <div class="max-w-3xl mx-auto w-full space-y-6">
    <UButton
      icon="i-lucide-arrow-left"
      variant="outline"
      color="neutral"
      @click="router.back()"
    >
      Назад
    </UButton>

    <div v-if="loading" class="flex justify-center py-12">
      <UIcon name="i-lucide-loader-2" class="w-8 h-8 animate-spin text-muted" />
    </div>

    <template v-else-if="request">
      <!-- Vendor info -->
      <div
        class="border border-gray-200 rounded-2xl p-6 bg-white flex items-center gap-4"
      >
        <div
          class="w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-base shrink-0"
          :style="{
            backgroundColor: avatarColor(
              request.vendor_profile.user?.company_name ?? '',
            ),
          }"
        >
          {{ initials(request.vendor_profile.user?.company_name ?? "") }}
        </div>
        <div>
          <NuxtLink
            :to="`/vendors/${request.vendor_profile.id}`"
            class="font-semibold text-base hover:underline"
          >
            {{ request.vendor_profile.user?.company_name }}
          </NuxtLink>
          <p class="text-sm text-gray-400">
            {{ request.vendor_profile.user?.full_name }}
          </p>
        </div>
        <div
          v-if="request.vendor_profile.rating"
          class="ml-auto flex items-center gap-1"
        >
          <UIcon
            name="i-lucide-star"
            class="w-4 h-4 text-amber-400 fill-amber-400"
          />
          <span class="font-semibold">{{
            request.vendor_profile.rating.toFixed(1)
          }}</span>
        </div>
      </div>

      <!-- Proposal details -->
      <div class="border border-gray-200 rounded-2xl p-6 bg-white space-y-5">
        <h3 class="font-semibold text-base">Предложение вендора</h3>
        <div class="grid grid-cols-3 gap-4">
          <div class="space-y-1">
            <p class="text-xs text-gray-400">Готов начать через</p>
            <p class="font-semibold text-lg">
              {{ request.days_to_start ?? "—" }} дн.
            </p>
          </div>
          <div class="space-y-1">
            <p class="text-xs text-gray-400">Длительность</p>
            <p class="font-semibold text-lg">
              {{ request.duration_days ?? "—" }} дн.
            </p>
          </div>
          <div class="space-y-1">
            <p class="text-xs text-gray-400">Стоимость</p>
            <p class="font-semibold text-lg">
              {{
                request.proposed_cost != null
                  ? "$" + request.proposed_cost.toLocaleString("ru-RU")
                  : "—"
              }}
            </p>
          </div>
        </div>
      </div>

      <!-- Project brief -->
      <ExistingProjectDetail :project-id="projectId" />

      <!-- Question answers -->
      <div
        v-if="request.question_answers?.length"
        class="border border-gray-200 rounded-2xl p-6 bg-white space-y-4"
      >
        <h3 class="font-semibold text-base">Ответы на вопросы</h3>
        <div
          v-for="(answer, i) in request.question_answers"
          :key="i"
          class="space-y-1"
        >
          <p class="text-sm font-medium text-gray-700">
            {{ i + 1 }}. {{ projectQuestions[i] }}
          </p>
          <p
            class="text-sm bg-gray-50 border border-gray-200 rounded-lg px-4 py-2.5"
          >
            {{ answer }}
          </p>
        </div>
      </div>

      <!-- Feasibility table -->
      <div
        v-if="request.feasibility_scores?.length"
        class="border border-gray-200 rounded-2xl p-6 bg-white space-y-4"
      >
        <h3 class="font-semibold text-base">Оценки выполнимости требований</h3>
        <div class="border border-gray-200 rounded-lg overflow-hidden">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th
                  class="text-left px-4 py-2.5 font-medium text-gray-600 w-1/4 border-r border-gray-200"
                >
                  Группа
                </th>
                <th class="text-left px-4 py-2.5 font-medium text-gray-600">
                  Требование
                </th>
                <th
                  class="text-center px-4 py-2.5 font-medium text-gray-600 w-24 border-l border-gray-200"
                >
                  Priority
                </th>
                <th
                  class="text-center px-4 py-2.5 font-medium text-gray-600 w-28 border-l border-gray-200"
                >
                  Feasibility
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in groupedFeasibilityRows"
                :key="row.origIndex"
                class="border-t border-gray-100"
              >
                <td
                  v-if="row.showGroup"
                  :rowspan="row.groupRowspan"
                  class="px-4 py-2.5 font-semibold border-r border-gray-200 align-middle"
                >
                  {{ row.score.group }}
                </td>
                <td class="px-4 py-2.5">{{ row.score.requirement }}</td>
                <td
                  class="px-4 py-2.5 text-center border-l border-gray-200 text-gray-500"
                >
                  {{ projectRequirements[row.origIndex]?.priority ?? "—" }}
                </td>
                <td
                  class="px-4 py-2.5 text-center border-l border-gray-200 font-semibold"
                >
                  {{ row.score.feasibility }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Accept / Deny -->
      <div class="flex justify-end gap-3">
        <template v-if="!alreadyProcessed">
          <UButton
            variant="outline"
            color="neutral"
            size="lg"
            @click="handleDeny"
          >
            Отклонить
          </UButton>
          <UButton size="lg" @click="handleAccept">
            Принять предложение
          </UButton>
        </template>
        <UButton v-else disabled size="lg">{{ alreadyProcessed }}</UButton>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import {
  requestsGetRequest,
  requestsAcceptProject,
  requestsDeclineProject,
  projectsGetProjectDetail,
} from "~/generated/api";
import type {
  ProjectRequestPublicVendorFull,
  RequirementItem,
} from "~/generated/api";

definePageMeta({
  layout: "dashboard",
  middleware: ["auth", "company-only"],
});

const route = useRoute();
const router = useRouter();
const projectId = route.params.project_id as string;
const requestId = route.params.request_id as string;

const loading = ref(true);
const request = ref<ProjectRequestPublicVendorFull | null>(null);
const projectQuestions = ref<string[]>([]);
const projectRequirements = ref<RequirementItem[]>([]);
const alreadyProcessed = ref<string | null>(null);
const toast = useToast();

const AVATAR_COLORS = [
  "#2563eb",
  "#16a34a",
  "#9333ea",
  "#db2777",
  "#d97706",
  "#0891b2",
  "#dc2626",
  "#059669",
  "#7c3aed",
  "#0284c7",
];

function avatarColor(name: string): string {
  let hash = 0;
  for (let i = 0; i < name.length; i++)
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length];
}

function initials(name: string): string {
  return name
    .split(" ")
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();
}

const groupedFeasibilityRows = computed(() => {
  const scores = request.value?.feasibility_scores ?? [];
  const groupOrder: string[] = [];
  const grouped = new Map<string, number[]>();
  scores.forEach((s, i) => {
    if (!grouped.has(s.group)) {
      grouped.set(s.group, []);
      groupOrder.push(s.group);
    }
    grouped.get(s.group)!.push(i);
  });
  const rows: {
    score: (typeof scores)[0];
    origIndex: number;
    showGroup: boolean;
    groupRowspan: number;
  }[] = [];
  for (const g of groupOrder) {
    const indices = grouped.get(g)!;
    indices.forEach((origIndex, j) => {
      rows.push({
        score: scores[origIndex],
        origIndex,
        showGroup: j === 0,
        groupRowspan: j === 0 ? indices.length : 0,
      });
    });
  }
  return rows;
});

onMounted(async () => {
  const [reqRes, projRes] = await Promise.all([
    requestsGetRequest({ path: { request_id: requestId } }),
    projectsGetProjectDetail({ path: { project_id: projectId } }),
  ]);
  loading.value = false;
  if (!reqRes.error) request.value = reqRes.data;
  if (!projRes.error) {
    projectQuestions.value = projRes.data.questions ?? [];
    projectRequirements.value = projRes.data.requirements ?? [];
  }
});

async function handleAccept() {
  const res = await requestsAcceptProject({ path: { request_id: requestId } });
  if (res.error) {
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(res.error),
      color: "error",
    });
    return;
  }
  toast.add({
    title: "Предложение принято",
    description: "Вендор получил уведомление.",
    color: "success",
  });
  alreadyProcessed.value = "Принято";
}

async function handleDeny() {
  const res = await requestsDeclineProject({ path: { request_id: requestId } });
  if (res.error) {
    toast.add({
      title: "Ошибка",
      description: extractErrorMessage(res.error),
      color: "error",
    });
    return;
  }
  toast.add({
    title: "Предложение отклонено",
    description: "Вендор получил уведомление.",
    color: "success",
  });
  alreadyProcessed.value = "Отклонено";
}
</script>
