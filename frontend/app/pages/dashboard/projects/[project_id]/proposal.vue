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

    <!-- Duration & Cost -->
    <div class="border border-gray-200 rounded-2xl p-6 bg-white space-y-6">
      <div class="space-y-4">
        <h3 class="font-semibold text-base">Сроки проекта</h3>
        <div class="grid grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Когда сможете начать</label>
            <div class="flex items-center border border-gray-300 rounded-lg overflow-hidden">
              <button
                class="px-4 py-2.5 text-lg font-medium text-gray-600 hover:bg-gray-100 transition"
                @click="daysToStart = Math.max(0, daysToStart - 1)"
              >−</button>
              <div class="flex-1 text-center py-2.5 text-sm font-medium">{{ daysToStart }} дн.</div>
              <button
                class="px-4 py-2.5 text-lg font-medium text-gray-600 hover:bg-gray-100 transition"
                @click="daysToStart++"
              >+</button>
            </div>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Сколько времени займёт</label>
            <div class="flex items-center border border-gray-300 rounded-lg overflow-hidden">
              <button
                class="px-4 py-2.5 text-lg font-medium text-gray-600 hover:bg-gray-100 transition"
                @click="durationDays = Math.max(1, durationDays - 1)"
              >−</button>
              <div class="flex-1 text-center py-2.5 text-sm font-medium">{{ durationDays }} дн.</div>
              <button
                class="px-4 py-2.5 text-lg font-medium text-gray-600 hover:bg-gray-100 transition"
                @click="durationDays++"
              >+</button>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-2">
        <h3 class="font-semibold text-base">Стоимость проекта</h3>
        <div class="flex items-center border border-gray-300 rounded-lg overflow-hidden max-w-xs">
          <button
            class="px-4 py-2.5 text-lg font-medium text-gray-600 hover:bg-gray-100 transition"
            @click="proposedCost = Math.max(0, proposedCost - 1000)"
          >−</button>
          <div class="flex-1 text-center py-2.5 text-sm font-medium">${{ proposedCost.toLocaleString('ru-RU') }}</div>
          <button
            class="px-4 py-2.5 text-lg font-medium text-gray-600 hover:bg-gray-100 transition"
            @click="proposedCost += 1000"
          >+</button>
        </div>
        <p class="text-xs text-gray-400">Шаг: $1 000. Можно ввести вручную.</p>
        <UInput
          v-model.number="proposedCost"
          type="number"
          min="0"
          step="1000"
          placeholder="Введите сумму"
          class="max-w-xs"
        />
      </div>
    </div>

    <!-- Question answers -->
    <div v-if="questions.length > 0" class="border border-gray-200 rounded-2xl p-6 bg-white space-y-4">
      <h3 class="font-semibold text-base">Вопросы от заказчика</h3>
      <p class="text-sm text-gray-500">Ответьте на все вопросы, чтобы отправить предложение.</p>
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
    <div v-if="requirements.length > 0" class="border border-gray-200 rounded-2xl p-6 bg-white space-y-4">
      <h3 class="font-semibold text-base">Оценка выполнимости требований</h3>
      <p class="text-sm text-gray-500">
        Укажите оценку выполнимости (1–10) для каждого требования. 1 — крайне сложно, 10 — без проблем.
      </p>
      <div class="border border-gray-200 rounded-lg overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-4 py-2.5 font-medium text-gray-600 w-1/4 border-r border-gray-200">
                Группа
              </th>
              <th class="text-left px-4 py-2.5 font-medium text-gray-600">
                Требование
              </th>
              <th class="text-center px-4 py-2.5 font-medium text-gray-600 w-24 border-l border-gray-200">
                Priority
              </th>
              <th class="text-center px-4 py-2.5 font-medium text-gray-600 w-28 border-l border-gray-200">
                Feasibility
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(req, i) in requirements"
              :key="i"
              class="border-t border-gray-100"
            >
              <td class="px-4 py-2.5 font-medium border-r border-gray-200 align-middle">
                {{ req.group }}
              </td>
              <td class="px-4 py-2.5">{{ req.requirement }}</td>
              <td class="px-4 py-2.5 text-center border-l border-gray-200 text-gray-500">
                {{ req.priority }}
              </td>
              <td class="px-4 py-2.5 border-l border-gray-200">
                <USelect
                  v-model="feasibilityScores[i]"
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
      <UButton
        :disabled="alreadySent || !canSubmit"
        :variant="alreadySent ? 'outline' : 'solid'"
        trailing-icon="i-lucide-arrow-right"
        @click="handleSendRequest"
      >
        {{ alreadySent ? 'Отправлено!' : 'Отправить предложение' }}
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { projectsSendProjectRequestVendor, projectsGetProjectDetail } from '~/generated/api';
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
  const res = await projectsGetProjectDetail({ path: { project_id: projectId } });
  if (res.error) return;

  questions.value = res.data.questions ?? [];
  requirements.value = res.data.requirements ?? [];
  questionAnswers.value = Array(questions.value.length).fill('');
  feasibilityScores.value = Array(requirements.value.length).fill('');
});

const allQuestionsAnswered = computed(() =>
  questions.value.every((_, i) => questionAnswers.value[i]?.trim())
);

const allFeasibilityFilled = computed(() =>
  requirements.value.every((_, i) => !!feasibilityScores.value[i])
);

const canSubmit = computed(
  () =>
    allQuestionsAnswered.value &&
    allFeasibilityFilled.value &&
    durationDays.value >= 1 &&
    proposedCost.value > 0
);

async function handleSendRequest() {
  const res = await projectsSendProjectRequestVendor({
    path: { project_id: projectId },
    body: {
      question_answers: questions.value.length > 0 ? questionAnswers.value : undefined,
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
      description: extractErrorMessage(res.error, 'Не удалось отправить предложение'),
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
