<template>
  <UButton @click="toggleTheme">
    {{ colorMode.value === 'dark' ? '🌙' : '☀️' }}
  </UButton>
</template>

<script setup>
const colorMode = useColorMode();

// Переключение темы
const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};
</script>
