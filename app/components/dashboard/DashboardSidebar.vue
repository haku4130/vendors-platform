<template>
  <aside class="w-64 bg-white border-r flex flex-col py-6 px-4">
    <!-- Аватар -->
    <UUser
      name="Osipov Andrey"
      description="Acme Corp"
      :avatar="{
        src: 'https://github.com/haku4130.png',
        icon: 'mdi:camera-outline',
        class: 'rounded-lg border border-black',
      }"
      size="3xl"
      class="px-4"
    />

    <!-- Кнопка редактирования -->
    <div class="w-full flex px-4">
      <button
        class="my-3 border border-black rounded-md px-3 py-1 text-sm font-medium hover:bg-black hover:text-white transition"
      >
        Edit Profile
      </button>
    </div>

    <!-- Навигация -->
    <nav class="flex flex-col gap-1 w-full">
      <button
        v-for="item in items"
        :key="item.label"
        :class="[
          'flex items-center justify-between w-full py-2 px-4 rounded-lg font-medium transition',
          selected === item.id
            ? 'bg-gray-100 text-black font-semibold'
            : 'hover:bg-gray-100 text-gray-800',
        ]"
        @click="$emit('select', item.id)"
      >
        <div class="flex items-center gap-3">
          <UIcon :name="item.icon" size="20" />
          <span>{{ item.label }}</span>
        </div>
        <span v-if="item.count !== undefined" class="text-sm">
          {{ item.count }}
        </span>
      </button>
    </nav>
  </aside>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
  selected: {
    type: String,
    default: '',
  },
});
defineEmits(['select']);
</script>
