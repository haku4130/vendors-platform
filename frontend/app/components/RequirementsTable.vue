<template>
  <div class="border border-gray-300 rounded-md overflow-hidden">
    <UTable :data="tableData" :columns="columns">
      <template #group-cell="{ row }">
        <UInput
          v-if="row.original.isAddRow"
          v-model="newItem.group"
          placeholder="Add a group"
          variant="ghost"
          size="sm"
          :ui="{ base: 'px-0' }"
        />
        <span v-else>{{ row.original.group }}</span>
      </template>

      <template #requirement-cell="{ row }">
        <UInput
          v-if="row.original.isAddRow"
          v-model="newItem.requirement"
          placeholder="Add a requirement"
          variant="ghost"
          size="sm"
          :ui="{ base: 'px-0' }"
          @keydown.enter="addItem"
        />
        <span v-else>{{ row.original.requirement }}</span>
      </template>

      <template #priority-cell="{ row }">
        <USelect
          v-if="row.original.isAddRow"
          v-model="newItem.priority"
          :items="priorityItems"
          placeholder="Priority"
          size="sm"
          class="w-full"
        />
        <USelect
          v-else-if="editing"
          :model-value="String(row.original.priority)"
          :items="priorityItems"
          size="sm"
          class="w-full"
          @update:model-value="
            updatePriority(row.original.index, Number($event))
          "
        />
        <span v-else class="flex justify-center">{{
          row.original.priority
        }}</span>
      </template>

      <template #actions-cell="{ row }">
        <UButton
          v-if="row.original.isAddRow"
          icon="i-lucide-plus"
          variant="ghost"
          color="neutral"
          size="sm"
          :disabled="!canAdd"
          @click="addItem"
        />
        <UButton
          v-else
          icon="i-lucide-x"
          variant="ghost"
          color="neutral"
          size="sm"
          @click="removeRequirement(row.original.index)"
        />
      </template>

      <template #empty>
        <p class="text-muted text-sm text-center py-3">{{ noItemsText }}</p>
      </template>
    </UTable>
  </div>
</template>

<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui';
import type { Cell } from '@tanstack/vue-table';
import type { Requirement } from '@/types/answers';

const modelValue = defineModel<Requirement[]>({ required: true });

const { editing = false, noItemsText = 'No requirements added yet.' } =
  defineProps<{
    editing?: boolean;
    noItemsText?: string;
  }>();

const priorityItems = ['1', '2', '3', '4', '5'];

type RowData = {
  group: string;
  requirement: string;
  priority: number;
  index: number;
  isAddRow?: true;
};

const tableData = computed((): RowData[] => {
  const groupOrder: string[] = [];
  const grouped = new Map<string, RowData[]>();

  modelValue.value.forEach((r, i) => {
    if (!grouped.has(r.group)) {
      grouped.set(r.group, []);
      groupOrder.push(r.group);
    }
    grouped.get(r.group)!.push({ ...r, index: i });
  });

  const rows: RowData[] = [];
  for (const g of groupOrder) rows.push(...grouped.get(g)!);

  if (editing) {
    rows.push({
      group: '',
      requirement: '',
      priority: 0,
      index: -1,
      isAddRow: true,
    });
  }

  return rows;
});

function getGroupRowSpan(cell: Cell<RowData, unknown>): string {
  const row = cell.row.original;
  if (row.isAddRow) return '1';

  const group = row.group;
  const rows = cell.getContext().table.getRowModel().rows;
  const idx = rows.findIndex((r) => r.id === cell.row.id);

  if (
    idx > 0 &&
    !rows[idx - 1]!.original.isAddRow &&
    rows[idx - 1]!.original.group === group
  ) {
    return '1';
  }

  let span = 1;
  for (let i = idx + 1; i < rows.length; i++) {
    if (!rows[i]!.original.isAddRow && rows[i]!.original.group === group)
      span++;
    else break;
  }
  return `${span}`;
}

function getGroupClass(cell: Cell<RowData, unknown>): string {
  const row = cell.row.original;

  const group = row.group;
  const rows = cell.getContext().table.getRowModel().rows;
  const idx = rows.findIndex((r) => r.id === cell.row.id);

  if (
    idx > 0 &&
    !rows[idx - 1]!.original.isAddRow &&
    rows[idx - 1]!.original.group === group
  ) {
    return 'hidden';
  }

  return 'font-semibold align-middle border-r border-default';
}

const columns = computed((): TableColumn<RowData>[] => {
  const cols: TableColumn<RowData>[] = [
    {
      accessorKey: 'group',
      header: 'Group of requirements',
      meta: {
        rowspan: { td: getGroupRowSpan },
        class: {
          th: 'border-r border-default w-1/4',
          td: getGroupClass,
        },
      },
    },
    {
      accessorKey: 'requirement',
      header: 'Business requirements',
    },
    {
      accessorKey: 'priority',
      header: 'Priority',
      meta: {
        class: {
          th: 'text-center border-l border-default w-28',
          td: 'text-center border-l border-default w-28',
        },
      },
    },
  ];

  if (editing) {
    cols.push({
      id: 'actions',
      meta: {
        class: {
          th: 'w-10',
          td: 'w-10 text-center',
        },
      },
    });
  }

  return cols;
});

const newItem = reactive({ group: '', requirement: '', priority: '' });
const canAdd = computed(
  () =>
    !!newItem.group.trim() &&
    !!newItem.requirement.trim() &&
    !!newItem.priority,
);

function addItem() {
  if (!canAdd.value) return;
  modelValue.value = [
    ...modelValue.value,
    {
      group: newItem.group.trim(),
      requirement: newItem.requirement.trim(),
      priority: Number(newItem.priority),
    },
  ];
  newItem.group = '';
  newItem.requirement = '';
  newItem.priority = '';
}

// Auto-commit pending add row when edit mode closes
watch(
  () => editing,
  (val) => {
    if (!val) addItem();
  },
);

function removeRequirement(index: number) {
  modelValue.value = modelValue.value.filter((_, i) => i !== index);
}

function updatePriority(index: number, priority: number) {
  const updated = [...modelValue.value];
  updated[index] = { ...updated[index]!, priority };
  modelValue.value = updated;
}
</script>
