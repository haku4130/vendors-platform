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

    <template v-else-if="proposal">
      <!-- Status badge -->
      <div class="flex items-center gap-3">
        <span
          :class="[
            'px-3 py-1 rounded-full text-sm font-semibold',
            statusStyle.bg,
            statusStyle.text,
          ]"
        >
          {{ statusStyle.label }}
        </span>
        <span class="text-sm text-gray-400"
          >Отправлено {{ formatDateReview(proposal.created_at) }}</span
        >
      </div>

      <!-- Project brief -->
      <ProjectDetail
        :data="projectAnswers"
        :company-name="proposal.project.owner.company_name"
        :contact-email="proposal.project.owner.email"
        :contact-name="proposal.project.owner.full_name"
      />

      <!-- Duration & Cost -->
      <div class="border border-gray-200 rounded-2xl p-6 bg-white space-y-5">
        <h3 class="font-semibold text-base">
          Ваше предложение по срокам и стоимости
        </h3>
        <div class="grid grid-cols-3 gap-4">
          <div class="space-y-1">
            <p class="text-xs text-gray-400">Готов начать через</p>
            <p class="font-semibold text-lg">
              {{ proposal.days_to_start ?? "—" }} дн.
            </p>
          </div>
          <div class="space-y-1">
            <p class="text-xs text-gray-400">Длительность</p>
            <p class="font-semibold text-lg">
              {{ proposal.duration_days ?? "—" }} дн.
            </p>
          </div>
          <div class="space-y-1">
            <p class="text-xs text-gray-400">Стоимость</p>
            <p class="font-semibold text-lg">
              {{
                proposal.proposed_cost != null
                  ? "$" + proposal.proposed_cost.toLocaleString("ru-RU")
                  : "—"
              }}
            </p>
          </div>
        </div>
      </div>

      <!-- Question answers -->
      <div
        v-if="proposal.project.questions?.length"
        class="border border-gray-200 rounded-2xl p-6 bg-white space-y-4"
      >
        <h3 class="font-semibold text-base">Ответы на вопросы заказчика</h3>
        <div
          v-for="(question, i) in proposal.project.questions"
          :key="i"
          class="space-y-1"
        >
          <p class="text-sm font-medium text-gray-700">
            {{ i + 1 }}. {{ question }}
          </p>
          <p
            class="text-sm bg-gray-50 border border-gray-200 rounded-lg px-4 py-2.5"
          >
            {{ proposal.question_answers?.[i] || "—" }}
          </p>
        </div>
      </div>

      <!-- Feasibility table -->
      <div
        v-if="proposal.project.requirements?.length"
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
                  {{ row.req.group }}
                </td>
                <td class="px-4 py-2.5">{{ row.req.requirement }}</td>
                <td
                  class="px-4 py-2.5 text-center border-l border-gray-200 text-gray-500"
                >
                  {{ row.req.priority }}
                </td>
                <td
                  class="px-4 py-2.5 text-center border-l border-gray-200 font-semibold"
                >
                  {{
                    proposal.feasibility_scores?.[row.origIndex]?.feasibility ??
                    "—"
                  }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { vendorsGetMyProposal } from "~/generated/api";
import type { ProjectRequestPublicProjectFull } from "~/generated/api";
import type { AnswersType } from "@/types/answers";

definePageMeta({
  layout: "dashboard",
  middleware: ["auth", "vendor-only"],
});

const route = useRoute();
const router = useRouter();
const requestId = route.params.request_id as string;

const loading = ref(true);
const proposal = ref<ProjectRequestPublicProjectFull | null>(null);

const STATUS_STYLES = {
  sent: { label: "На рассмотрении", bg: "bg-amber-50", text: "text-amber-700" },
  accepted: { label: "Принято", bg: "bg-green-50", text: "text-green-700" },
  declined: { label: "Отклонено", bg: "bg-red-50", text: "text-red-600" },
} as const;

const statusStyle = computed(() => {
  const s = proposal.value?.status as keyof typeof STATUS_STYLES;
  return STATUS_STYLES[s] ?? STATUS_STYLES.sent;
});

const groupedFeasibilityRows = computed(() => {
  const reqs = proposal.value?.project.requirements ?? [];
  const groupOrder: string[] = [];
  const grouped = new Map<string, number[]>();
  reqs.forEach((r, i) => {
    if (!grouped.has(r.group)) {
      grouped.set(r.group, []);
      groupOrder.push(r.group);
    }
    grouped.get(r.group)!.push(i);
  });
  const rows: {
    req: (typeof reqs)[0];
    origIndex: number;
    showGroup: boolean;
    groupRowspan: number;
  }[] = [];
  for (const g of groupOrder) {
    const indices = grouped.get(g)!;
    indices.forEach((origIndex, j) => {
      rows.push({
        req: reqs[origIndex],
        origIndex,
        showGroup: j === 0,
        groupRowspan: j === 0 ? indices.length : 0,
      });
    });
  }
  return rows;
});

const projectAnswers = computed<AnswersType | null>(() => {
  const p = proposal.value?.project;
  if (!p) return null;
  return {
    projectName: p.title,
    projectIntroduction: p.description ?? "",
    startTime: p.start_date ?? "",
    exactLocation: p.location ?? null,
    website: p.website ?? "",
    servicesNeeded: p.services ?? [],
    budget: p.budget ?? 0,
    questions: p.questions ?? [],
    requirements: p.requirements ?? [],
  };
});

onMounted(async () => {
  const res = await vendorsGetMyProposal({ path: { request_id: requestId } });
  loading.value = false;
  if (!res.error) proposal.value = res.data;
});
</script>
