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

    <ExistingProjectDetail :project-id="projectId" />

    <!-- Sent confirmation -->
    <div
      v-if="alreadySent"
      class="border border-green-200 rounded-2xl p-6 bg-green-50 space-y-4"
    >
      <div class="flex items-center gap-2 text-green-700">
        <UIcon name="i-lucide-circle-check" class="w-5 h-5 shrink-0" />
        <h3 class="font-semibold text-base">Предложение отправлено</h3>
      </div>
      <div class="grid grid-cols-3 gap-4">
        <div class="space-y-1">
          <p class="text-xs text-gray-500">Готов начать через</p>
          <p class="font-semibold">{{ daysToStart }} дн.</p>
        </div>
        <div class="space-y-1">
          <p class="text-xs text-gray-500">Длительность</p>
          <p class="font-semibold">{{ durationDays }} дн.</p>
        </div>
        <div class="space-y-1">
          <p class="text-xs text-gray-500">Стоимость</p>
          <p class="font-semibold">
            ${{ proposedCost.toLocaleString('ru-RU') }}
          </p>
        </div>
      </div>
      <div
        v-if="questions.length > 0"
        class="space-y-3 pt-2 border-t border-green-200"
      >
        <p class="text-sm font-medium text-gray-700">Ваши ответы на вопросы:</p>
        <div v-for="(q, i) in questions" :key="i" class="space-y-0.5">
          <p class="text-xs text-gray-500">{{ i + 1 }}. {{ q }}</p>
          <p class="text-sm">{{ questionAnswers[i] }}</p>
        </div>
      </div>
      <div
        v-if="requirements.length > 0"
        class="space-y-3 pt-2 border-t border-green-200"
      >
        <p class="text-sm font-medium text-gray-700">Оценки выполнимости:</p>
        <div class="border border-green-200 rounded-lg overflow-hidden">
          <table class="w-full text-sm">
            <thead class="bg-green-100 border-b border-green-200">
              <tr>
                <th
                  class="text-left px-4 py-2 font-medium text-gray-600 w-1/4 border-r border-green-200"
                >
                  Группа
                </th>
                <th class="text-left px-4 py-2 font-medium text-gray-600">
                  Требование
                </th>
                <th
                  class="text-center px-4 py-2 font-medium text-gray-600 w-24 border-l border-green-200"
                >
                  Priority
                </th>
                <th
                  class="text-center px-4 py-2 font-medium text-gray-600 w-28 border-l border-green-200"
                >
                  Feasibility
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in groupedFeasibilityRows"
                :key="row.origIndex"
                class="border-t border-green-100"
              >
                <td
                  v-if="row.showGroup"
                  :rowspan="row.groupRowspan"
                  class="px-4 py-2 font-semibold border-r border-green-200 align-middle"
                >
                  {{ row.req.group }}
                </td>
                <td class="px-4 py-2">{{ row.req.requirement }}</td>
                <td
                  class="px-4 py-2 text-center border-l border-green-200 text-gray-500"
                >
                  {{ row.req.priority }}
                </td>
                <td
                  class="px-4 py-2 text-center border-l border-green-200 font-semibold"
                >
                  {{ feasibilityScores[row.origIndex] || '—' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <template v-if="!alreadySent">
      <!-- Duration & Cost -->
      <div class="border border-gray-200 rounded-2xl p-6 bg-white space-y-6">
        <div class="space-y-4">
          <h3 class="font-semibold text-base">Сроки проекта</h3>
          <div class="grid grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700"
                >Когда сможете начать</label
              >
              <UInputNumber
                v-model="daysToStart"
                :min="0"
                :default-value="0"
                locale="ru-RU"
                :format-options="{ style: 'unit', unit: 'day' }"
                color="neutral"
                class="w-full"
              />
            </div>
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700"
                >Сколько времени займёт</label
              >
              <UInputNumber
                v-model="durationDays"
                :min="1"
                :default-value="1"
                locale="ru-RU"
                :format-options="{ style: 'unit', unit: 'day' }"
                color="neutral"
                class="w-full"
              />
            </div>
          </div>
        </div>

        <div class="space-y-2">
          <h3 class="font-semibold text-base">Стоимость проекта</h3>
          <UInputNumber
            v-model="proposedCost"
            :min="0"
            :default-value="0"
            :format-options="{
              style: 'currency',
              currency: 'USD',
              currencyDisplay: 'narrowSymbol',
              minimumFractionDigits: 0,
              maximumFractionDigits: 0,
            }"
            color="neutral"
            class="max-w-xs"
          />
        </div>
      </div>

      <!-- Question answers -->
      <div
        v-if="questions.length > 0"
        class="border border-gray-200 rounded-2xl p-6 bg-white space-y-4"
      >
        <h3 class="font-semibold text-base">Вопросы от заказчика</h3>
        <p class="text-sm text-gray-500">
          Ответьте на все вопросы, чтобы отправить предложение.
        </p>
        <div v-for="(question, i) in questions" :key="i" class="space-y-1">
          <label class="text-sm font-medium">{{ i + 1 }}. {{ question }}</label>
          <UTextarea
            v-model="questionAnswers[i]"
            :placeholder="`Ответ на вопрос ${i + 1}`"
            :rows="3"
            class="w-full"
          />
        </div>
      </div>

      <!-- Feasibility table -->
      <div
        v-if="requirements.length > 0"
        class="border border-gray-200 rounded-2xl p-6 bg-white space-y-4"
      >
        <h3 class="font-semibold text-base">Оценка выполнимости требований</h3>
        <p class="text-sm text-gray-500">
          Укажите оценку выполнимости (1–10) для каждого требования. 1 — крайне
          сложно, 10 — без проблем.
        </p>
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
                <td class="px-4 py-2.5 border-l border-gray-200">
                  <USelect
                    v-model="feasibilityScores[row.origIndex]"
                    :items="feasibilityOptions"
                    placeholder="—"
                    size="sm"
                    class="w-full"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="flex justify-end">
        <UTooltip
          :delay-duration="0"
          :text="submitTooltip"
          :disabled="canSubmit"
          :disable-closing-trigger="true"
        >
          <UButton
            :disabled="!canSubmit"
            trailing-icon="i-lucide-arrow-right"
            @click="handleSendRequest"
          >
            Отправить предложение
          </UButton>
        </UTooltip>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import {
  projectsSendProjectRequestVendor,
  projectsGetProjectDetail,
} from '~/generated/api';
import type { RequirementItem } from '~/generated/api';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', 'vendor-only'],
});

const route = useRoute();
const router = useRouter();
const projectId = route.params.project_id as string;

const alreadySent = ref(false);
const toast = useToast();

const questions = ref<string[]>([]);
const requirements = ref<RequirementItem[]>([]);

const questionAnswers = ref<string[]>([]);
const feasibilityScores = ref<string[]>([]);

const daysToStart = ref(0);
const durationDays = ref(1);
const proposedCost = ref(0);

const feasibilityOptions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];

onMounted(async () => {
  const res = await projectsGetProjectDetail({
    path: { project_id: projectId },
  });
  if (res.error) return;

  questions.value = res.data.questions ?? [];
  requirements.value = res.data.requirements ?? [];
  questionAnswers.value = Array(questions.value.length).fill('');
  feasibilityScores.value = Array(requirements.value.length).fill('');
});

const groupedFeasibilityRows = computed(() => {
  const groupOrder: string[] = [];
  const grouped = new Map<string, number[]>();
  requirements.value.forEach((r, i) => {
    if (!grouped.has(r.group)) {
      grouped.set(r.group, []);
      groupOrder.push(r.group);
    }
    grouped.get(r.group)!.push(i);
  });
  const rows: {
    req: (typeof requirements.value)[0];
    origIndex: number;
    showGroup: boolean;
    groupRowspan: number;
  }[] = [];
  for (const g of groupOrder) {
    const indices = grouped.get(g)!;
    indices.forEach((origIndex, j) => {
      rows.push({
        req: requirements.value[origIndex],
        origIndex,
        showGroup: j === 0,
        groupRowspan: j === 0 ? indices.length : 0,
      });
    });
  }
  return rows;
});

const allQuestionsAnswered = computed(() =>
  questions.value.every((_, i) => questionAnswers.value[i]?.trim()),
);

const allFeasibilityFilled = computed(() =>
  requirements.value.every((_, i) => !!feasibilityScores.value[i]),
);

const canSubmit = computed(
  () =>
    allQuestionsAnswered.value &&
    allFeasibilityFilled.value &&
    durationDays.value >= 1 &&
    proposedCost.value > 0,
);

const submitTooltip = computed(() => {
  const missing: string[] = [];
  if (proposedCost.value <= 0) missing.push('укажите стоимость проекта');
  if (durationDays.value < 1) missing.push('укажите длительность');
  if (!allQuestionsAnswered.value) missing.push('ответьте на все вопросы');
  if (!allFeasibilityFilled.value) missing.push('оцените все требования');
  return missing.length ? 'Чтобы отправить: ' + missing.join(', ') : '';
});

async function handleSendRequest() {
  const res = await projectsSendProjectRequestVendor({
    path: { project_id: projectId },
    body: {
      question_answers:
        questions.value.length > 0 ? questionAnswers.value : undefined,
      feasibility_scores:
        requirements.value.length > 0
          ? requirements.value.map((req, i) => ({
              group: req.group,
              requirement: req.requirement,
              feasibility: Number(feasibilityScores.value[i]),
            }))
          : undefined,
      days_to_start: daysToStart.value,
      duration_days: durationDays.value,
      proposed_cost: proposedCost.value,
    },
  });

  if (res.error) {
    toast.add({
      title: 'Ошибка',
      description: extractErrorMessage(
        res.error,
        'Не удалось отправить предложение',
      ),
      color: 'error',
    });
    return;
  }

  toast.add({
    title: 'Предложение отправлено',
    description: 'Заказчик получил уведомление.',
    color: 'success',
  });
  alreadySent.value = true;
}
</script>
