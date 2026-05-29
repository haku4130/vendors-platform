<template>
  <UHeader>
    <template #title>
      <NuxtLink :to="$localePath('/')" class="flex items-center gap-2 font-bold text-blue-600">
        <Logo />
        {{ $t('brandName') }}
      </NuxtLink>
    </template>

    <template #right>
      <LangSwitcher />
      <div class="hidden items-center gap-2 md:flex">
        <template v-if="auth.user.value">
          <UButton :to="$localePath('/dashboard/projects')">{{ $t('nav.dashboard') }}</UButton>
        </template>
        <template v-else>
          <UButton :to="$localePath('/sign-in')">{{ $t('nav.signIn') }}</UButton>
          <UButton :to="$localePath('/register')" variant="solid">{{ $t('nav.getStarted') }}</UButton>
        </template>
      </div>
    </template>

    <template #body>
      <LangSwitcher />
      <div class="flex flex-col gap-2 p-4">
        <template v-if="auth.user.value">
          <UButton :to="$localePath('/dashboard/projects')" block>{{ $t('nav.dashboard') }}</UButton>
        </template>
        <template v-else>
          <UButton :to="$localePath('/sign-in')" block>{{ $t('nav.signIn') }}</UButton>
          <UButton :to="$localePath('/register')" variant="solid" block>{{ $t('nav.getStarted') }}</UButton>
        </template>
      </div>
    </template>
  </UHeader>
</template>

<script setup lang="ts">
const auth = useAuth();
</script>
